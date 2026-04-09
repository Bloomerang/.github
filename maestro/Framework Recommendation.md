# Mobile Automation Framework Recommendation

**Recommendation:** Maestro  
**Status:** Proposed  
**Author:** QA  
**Teams:** .NET MAUI Mobile, React Native Mobile

---

## Decision

The team should adopt **Maestro** as the shared mobile automation framework across both the .NET MAUI and React Native apps.

---

## Context

Both mobile teams are moving to a model where developers write and own automated tests. The framework needs to support that — it should be easy to learn, easy to read, and quick to set up, so developers can contribute without a steep onboarding ramp.

Three tools were evaluated: Appium, Appium MCP, and Maestro. A full comparison is available in [Mobile Automation Tools](./Mobile%20Automation%20Tools.md).

---

## Why Maestro

### 1. Developers can write tests without becoming automation specialists

Maestro tests are written in YAML — a plain, readable format with no traditional programming required. A developer who has never written a UI test can read an existing flow, understand it immediately, and write a new one within an hour. Appium requires learning a framework, configuring a local server, and writing code in a test-specific style on top of normal development work. That friction is a real barrier when test authorship is distributed across the team.

### 2. React Native support is mature and well-tested

Maestro was built with React Native as a primary target. The React Native team gets a framework with strong community usage and documented patterns from day one.

### 3. The automation boundaries we've already defined remove the hardest MAUI concerns

Maestro's .NET MAUI support is less established than its React Native support. However, our [Automation Test Plan](./Automation%20Test%20Plan.md) already scopes out the areas where MAUI automation is most uncertain — NFC/Tap to Pay, external card readers, and biometrics. What remains in scope is login flows, navigation, form inputs, API-driven content, and regression scenarios. These are well within what Maestro handles on MAUI today.

### 4. Setup takes minutes, not days

Getting Appium running requires installing and configuring a local server, platform drivers, and language bindings before writing a single test. Maestro installs in one command. Teams should be writing real tests, not configuring infrastructure.

### 5. CI/CD integration is straightforward

Maestro has first-class support for running in CI pipelines. Tests can run on emulators/simulators in CI and on real devices via cloud providers (Maestro Cloud, BrowserStack, etc.).

---

## Why Not the Alternatives

**Appium** — the right choice for teams that need deep device access, complex multi-app scenarios, or advanced test logic. That's not where we're starting. The setup complexity and learning curve work against a model where developers are the primary test authors.

**Appium MCP** — interesting for AI-assisted test generation, but it's a thin layer on top of Appium. All of Appium's underlying complexity remains, and troubleshooting still requires Appium expertise. The community is very small and the tool is early-stage. Not the right foundation for a team building automation for the first time.

---

## Risk: .NET MAUI Proof of Concept Required

Before the MAUI team begins writing tests at scale, we need to validate that Maestro can reliably interact with MAUI's accessibility layer on real devices.

**Proposed validation sprint:**

| Step | Detail |
|------|--------|
| Target flow | Login → dashboard (one stable, representative flow) |
| Device | One iOS device, one Android device |
| Goal | Confirm `AutomationId` values in XAML are correctly exposed and targetable by Maestro |
| Exit criteria | Test runs reliably 5/5 times on each platform |
| Fallback | If MAUI accessibility gaps are significant, re-evaluate Appium for the MAUI team only |

This is a small investment that either confirms the choice or surfaces a real problem before the team is committed.

---

## What Developers Need to Do

1. **Set `AutomationId` on interactive elements** in MAUI XAML and React Native components. Maestro targets elements by this ID. Without it, tests are fragile.
2. **Follow the automation standards** that will be published alongside the framework setup — naming conventions, assertion patterns, what makes a test worth writing.
3. **Write tests for new features** as part of the definition of done, not as a separate follow-up.

QA will provide the framework setup, standards documentation, example flows, and ongoing review of test quality during PR review.

---

## What QA Will Provide

- Maestro workspace setup and CI integration
- Automation standards documentation
- Example flows for common patterns (login, form submission, navigation)
- PR review feedback on test coverage and quality
- The proof-of-concept validation for MAUI

---

## Next Steps

| Action | Owner | When |
|--------|-------|------|
| Run MAUI proof-of-concept sprint | QA + MAUI team lead | Before automation kickoff |
| Publish automation standards doc | QA | Alongside framework setup |
| Establish `AutomationId` conventions in MAUI XAML | MAUI team | Sprint following PoC |
| First developer-authored tests | Both teams | After standards published |

---

## Related Documents

- [Mobile Automation Tools](./Mobile%20Automation%20Tools.md) — full framework comparison
- [Automation Test Plan](./Automation%20Test%20Plan.md) — what to automate, what not to, and how to prioritize
- [Quality Readiness Plan](./Quality%20Readiness%20Plan.md) — business rules inventory, API dependency mapping, hardware boundary definition
