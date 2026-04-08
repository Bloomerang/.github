#!/usr/bin/env python3
"""
Jira / Xray Test Uploader

Uploads test results (JUnit XML, Cucumber JSON, Xray JSON) or creates
new test cases in Xray via the Jira REST API or Xray Cloud API.

Required environment variables:
  JIRA_BASE_URL      - e.g. https://yourcompany.atlassian.net
  JIRA_USERNAME      - Jira username or email
  JIRA_API_TOKEN     - Jira API token
  JIRA_PROJECT_KEY   - e.g. PROJ

Optional (Xray Cloud):
  XRAY_CLIENT_ID     - Xray Cloud client ID
  XRAY_CLIENT_SECRET - Xray Cloud client secret
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_ENV_VARS = ["JIRA_BASE_URL", "JIRA_USERNAME", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"]
XRAY_CLOUD_TOKEN_URL = "https://xray.cloud.getxpand.io/api/v2/authenticate"
XRAY_CLOUD_BASE_URL = "https://xray.cloud.getxpand.io/api/v2"


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

def get_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


def check_env() -> bool:
    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v, "").strip()]
    if missing:
        print("ERROR: Missing required environment variables:")
        for v in missing:
            print(f"  {v}")
        print("\nSet them in your shell or CI environment before running this script.")
        print("Jira API tokens: https://id.atlassian.com/manage/api-tokens")
        return False

    optional_missing = []
    for v in ("XRAY_CLIENT_ID", "XRAY_CLIENT_SECRET"):
        if not os.environ.get(v, "").strip():
            optional_missing.append(v)
    if optional_missing:
        print("INFO: Xray Cloud variables not set (needed only for Xray Cloud API):")
        for v in optional_missing:
            print(f"  {v}")
        print("  Falling back to Jira Server/DC API.\n")

    print("Environment OK.")
    return True


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _basic_auth_header(username: str, token: str) -> str:
    credentials = base64.b64encode(f"{username}:{token}".encode()).decode()
    return f"Basic {credentials}"


def _bearer_header(token: str) -> str:
    return f"Bearer {token}"


def http_request(
    url: str,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict | None = None,
) -> dict:
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            return {"status": resp.status, "body": json.loads(body) if body else {}}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(
            f"HTTP {e.code} {e.reason} for {url}\n{body}"
        ) from e


# ---------------------------------------------------------------------------
# Xray Cloud authentication
# ---------------------------------------------------------------------------

def get_xray_cloud_token(client_id: str, client_secret: str) -> str:
    payload = json.dumps(
        {"client_id": client_id, "client_secret": client_secret}
    ).encode()
    result = http_request(
        XRAY_CLOUD_TOKEN_URL,
        method="POST",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    # Response body is a plain JSON string (the token)
    token = result["body"]
    if isinstance(token, str):
        return token.strip('"')
    raise RuntimeError(f"Unexpected token response: {token}")


# ---------------------------------------------------------------------------
# JUnit XML parsing
# ---------------------------------------------------------------------------

def parse_junit_xml(file_path: str) -> dict:
    """Parse JUnit XML into an Xray-compatible test execution payload."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Support both <testsuite> and <testsuites> as root
    suites = (
        [root] if root.tag == "testsuite"
        else root.findall("testsuite")
    )

    tests = []
    for suite in suites:
        for tc in suite.findall("testcase"):
            name = tc.get("name", "Unnamed test")
            classname = tc.get("classname", "")
            full_name = f"{classname}.{name}" if classname else name

            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if skipped is not None:
                status = "TODO"
                comment = skipped.get("message", "Skipped")
            elif failure is not None:
                status = "FAIL"
                comment = failure.get("message", "") or (failure.text or "")
            elif error is not None:
                status = "FAIL"
                comment = error.get("message", "") or (error.text or "")
            else:
                status = "PASS"
                comment = ""

            tests.append(
                {
                    "testInfo": {"summary": full_name},
                    "status": status,
                    "comment": comment[:2000] if comment else "",
                }
            )

    return {"tests": tests}


# ---------------------------------------------------------------------------
# Cucumber JSON parsing
# ---------------------------------------------------------------------------

def parse_cucumber_json(file_path: str) -> list:
    """Return raw Cucumber JSON suitable for Xray's import endpoint."""
    with open(file_path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Xray JSON (test cases) loading
# ---------------------------------------------------------------------------

def load_xray_test_cases(file_path: str) -> list:
    with open(file_path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "tests" in data:
        return data["tests"]
    raise ValueError(
        f"Unexpected test-cases JSON structure in {file_path}. "
        "Expected a list or {\"tests\": [...]}."
    )


# ---------------------------------------------------------------------------
# Upload: test results (JUnit / Cucumber) via Xray Cloud API
# ---------------------------------------------------------------------------

def upload_junit_xray_cloud(
    token: str, results: dict, project_key: str, execution_key: str | None
) -> dict:
    url = f"{XRAY_CLOUD_BASE_URL}/import/execution"
    payload = {
        "testExecutionInfo": {
            "project": {"key": project_key},
            "summary": "Test Execution",
        },
        "tests": results["tests"],
    }
    if execution_key:
        payload["testExecutionInfo"]["key"] = execution_key

    return http_request(
        url,
        method="POST",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": _bearer_header(token),
        },
    )


def upload_cucumber_xray_cloud(
    token: str, cucumber_data: list, project_key: str, execution_key: str | None
) -> dict:
    url = f"{XRAY_CLOUD_BASE_URL}/import/execution/cucumber"
    params = {"projectKey": project_key}
    if execution_key:
        params["testExecKey"] = execution_key
    url = f"{url}?{urllib.parse.urlencode(params)}"

    return http_request(
        url,
        method="POST",
        data=json.dumps(cucumber_data).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": _bearer_header(token),
        },
    )


# ---------------------------------------------------------------------------
# Upload: test results via Jira Server/DC (Xray Server REST API)
# ---------------------------------------------------------------------------

def upload_junit_xray_server(
    base_url: str,
    auth_header: str,
    results: dict,
    project_key: str,
    execution_key: str | None,
) -> dict:
    url = f"{base_url}/rest/raven/1.0/import/execution"
    payload = {
        "testExecutionInfo": {
            "project": project_key,
            "summary": "Test Execution",
        },
        "tests": results["tests"],
    }
    if execution_key:
        payload["testExecutionInfo"]["testExecutionKey"] = execution_key

    return http_request(
        url,
        method="POST",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_header,
        },
    )


def upload_cucumber_xray_server(
    base_url: str,
    auth_header: str,
    cucumber_data: list,
    project_key: str,
    execution_key: str | None,
) -> dict:
    url = f"{base_url}/rest/raven/1.0/import/execution/cucumber"
    params = {"projectKey": project_key}
    if execution_key:
        params["testExecKey"] = execution_key
    url = f"{url}?{urllib.parse.urlencode(params)}"

    return http_request(
        url,
        method="POST",
        data=json.dumps(cucumber_data).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_header,
        },
    )


# ---------------------------------------------------------------------------
# Create test cases via Jira REST API (works for both Cloud and Server)
# ---------------------------------------------------------------------------

def create_test_cases(
    base_url: str,
    auth_header: str,
    project_key: str,
    test_cases: list,
) -> list:
    """Create Xray Test issues via the Jira issue creation endpoint."""
    created = []
    url = f"{base_url}/rest/api/2/issue"

    for tc in test_cases:
        test_info = tc.get("testInfo", tc)
        summary = test_info.get("summary", "Untitled Test")
        description = test_info.get("description", "")

        # Build Xray manual test steps (stored as a custom field in Xray)
        steps = test_info.get("steps", [])
        steps_text = "\n".join(
            f"Step {i + 1}: {s.get('action', '')} | Expected: {s.get('result', '')}"
            for i, s in enumerate(steps)
        )
        if steps_text:
            description = f"{description}\n\n{steps_text}".strip()

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Test"},
            }
        }

        result = http_request(
            url,
            method="POST",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": auth_header,
            },
        )
        issue = result["body"]
        created.append({"key": issue.get("key"), "summary": summary})
        print(f"  Created: {issue.get('key')} — {summary}")

    return created


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload test results or create test cases in Xray (Jira)."
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Verify required environment variables are set and exit.",
    )
    parser.add_argument(
        "--type",
        choices=["junit", "cucumber", "create-tests"],
        help="Type of upload: junit | cucumber | create-tests",
    )
    parser.add_argument(
        "--file",
        help="Path to the result or test-cases file.",
    )
    parser.add_argument(
        "--project-key",
        help="Jira project key (overrides JIRA_PROJECT_KEY env var).",
    )
    parser.add_argument(
        "--test-execution-key",
        help="Existing Test Execution issue key to attach results to.",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.check_env:
        ok = check_env()
        sys.exit(0 if ok else 1)

    if not args.type or not args.file:
        parser.error("--type and --file are required unless using --check-env")

    # Verify env
    if not check_env():
        sys.exit(1)

    base_url = get_env("JIRA_BASE_URL").rstrip("/")
    username = get_env("JIRA_USERNAME")
    api_token = get_env("JIRA_API_TOKEN")
    project_key = args.project_key or get_env("JIRA_PROJECT_KEY")
    execution_key = args.test_execution_key

    auth_header = _basic_auth_header(username, api_token)

    xray_client_id = os.environ.get("XRAY_CLIENT_ID", "").strip()
    xray_client_secret = os.environ.get("XRAY_CLIENT_SECRET", "").strip()
    use_xray_cloud = bool(xray_client_id and xray_client_secret)

    file_path = args.file
    if not Path(file_path).exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading '{file_path}' (type={args.type}) to project {project_key}...")
    if use_xray_cloud:
        print("Using Xray Cloud API.")
        xray_token = get_xray_cloud_token(xray_client_id, xray_client_secret)
    else:
        print("Using Jira Server/DC API (no XRAY_CLIENT_ID/SECRET set).")

    # ---- JUnit ----
    if args.type == "junit":
        results = parse_junit_xml(file_path)
        total = len(results["tests"])
        passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
        failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
        print(f"Parsed {total} tests: {passed} passed, {failed} failed.")

        if use_xray_cloud:
            resp = upload_junit_xray_cloud(xray_token, results, project_key, execution_key)
        else:
            resp = upload_junit_xray_server(base_url, auth_header, results, project_key, execution_key)

        body = resp["body"]
        exec_key = body.get("key") or body.get("testExecIssue", {}).get("key", "?")
        print(f"Success! Test Execution: {base_url}/browse/{exec_key}")

    # ---- Cucumber ----
    elif args.type == "cucumber":
        cucumber_data = parse_cucumber_json(file_path)
        print(f"Parsed {len(cucumber_data)} feature(s).")

        if use_xray_cloud:
            resp = upload_cucumber_xray_cloud(xray_token, cucumber_data, project_key, execution_key)
        else:
            resp = upload_cucumber_xray_server(base_url, auth_header, cucumber_data, project_key, execution_key)

        body = resp["body"]
        exec_key = body.get("key") or body.get("testExecIssue", {}).get("key", "?")
        print(f"Success! Test Execution: {base_url}/browse/{exec_key}")

    # ---- Create test cases ----
    elif args.type == "create-tests":
        test_cases = load_xray_test_cases(file_path)
        print(f"Creating {len(test_cases)} test case(s) in project {project_key}...")
        created = create_test_cases(base_url, auth_header, project_key, test_cases)
        print(f"\nDone. Created {len(created)} test issue(s).")
        for tc in created:
            print(f"  {base_url}/browse/{tc['key']}  —  {tc['summary']}")


if __name__ == "__main__":
    main()
