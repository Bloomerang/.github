# Test Plan Skill

Generate a comprehensive, Xray-compatible test plan for a feature, component, or user story.

## Trigger Conditions

Invoke this skill when the user asks to:
- Create or generate a test plan
- Write test cases for a feature or component
- Generate tests for Xray / Jira
- Document test coverage for a PR or story

## Steps

1. **Determine scope**

   If the user did not specify what to test, ask:
   - What feature, component, or user story needs coverage?
   - Is there a Jira issue key to link the tests to?
   - Should tests be manual, automated, or both?

   Otherwise infer scope from:
   - Recent git changes (`git diff main...HEAD --name-only`)
   - Any Jira issue key mentioned by the user
   - Files open or referenced in the conversation

2. **Analyze the code**

   Read the relevant source files. Identify:
   - Public API surface (functions, endpoints, UI interactions)
   - Business logic and decision branches
   - External dependencies (APIs, databases, services)
   - Error paths and validation rules

3. **Generate test cases**

   For each area of the code, produce test cases that cover:
   - **Happy path**: expected inputs produce expected outputs
   - **Edge cases**: boundary values, empty inputs, max/min values
   - **Error conditions**: invalid inputs, failures, timeouts
   - **Integration points**: interactions with external systems

   Each test case must include:
   | Field | Description |
   |-------|-------------|
   | Summary | One-line description of what is being tested |
   | Preconditions | State required before executing the test |
   | Steps | Numbered list of actions |
   | Expected Result | Observable outcome that indicates pass |
   | Priority | Critical / High / Medium / Low |
   | Type | Manual / Automated |

4. **Present the test plan**

   Display test cases as a readable Markdown table or numbered list grouped by feature area. Include a summary row count (e.g., "12 test cases: 3 Critical, 5 High, 4 Medium").

5. **Offer Xray export**

   After presenting the plan, ask:
   > "Would you like to export these test cases as Xray-compatible JSON so they can be uploaded to Jira?"

   If yes, emit a JSON file named `test-plan.json` in the current directory with this structure:

   ```json
   {
     "tests": [
       {
         "testInfo": {
           "summary": "Test case summary",
           "description": "Optional detail",
           "testType": "Manual",
           "steps": [
             {
               "action": "Action to perform",
               "data": "Input data (optional)",
               "result": "Expected result"
             }
           ]
         },
         "xray_test_sets": []
       }
     ]
   }
   ```

   Then ask:
   > "Would you like to upload these test cases to Xray now? I can run the xray-upload skill."

## Notes

- Prefer concrete, observable expected results over vague ones ("returns HTTP 200" not "works correctly").
- Do not generate tests for code you have not read.
- Keep test cases independent — each should be runnable in isolation.
- If the user provides a Jira issue key (e.g., `PROJ-42`), include it in the description of each test case for traceability.
