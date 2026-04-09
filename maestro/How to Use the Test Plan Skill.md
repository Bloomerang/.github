# How to Use the Test Plan Skill

This guide walks you through generating a manual test plan from a Jira ticket using Claude Code.

---

## Prerequisites (Do These First)

These are one-time steps to get your machine set up. If you've already done them, skip ahead to [Before You Start](#before-you-start-one-time-setup).

### 1. Install WSL and Ubuntu

1. Press the Windows key, type `powershell`, right-click **Windows PowerShell** → **Run as administrator**
2. Run:
   ```
   wsl --install
   ```
3. Restart your computer when it finishes
4. After restart, Ubuntu opens automatically — create a username and password when prompted
   > When typing your password, nothing appears on screen — that's normal

---

### 2. Install Node.js and Claude Code

Open the Ubuntu terminal and run these one at a time:

```bash
sudo apt update
sudo apt upgrade -y
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

Then launch it:
```bash
claude
```

On first launch it will ask you to log in — use your Bloomerang Claude Enterprise account.

---

### 3. Authenticate with GitHub

In the Ubuntu terminal (outside Claude Code):

```bash
sudo apt install gh -y
gh auth login
```

When prompted:
- **Where do you use GitHub?** → `GitHub.com`
- **Preferred protocol?** → `HTTPS`
- **Authenticate with browser?** → `Yes`

A code will appear in the terminal. Open `https://github.com/login/device` in your browser, enter the code, and log in with your Bloomerang GitHub account.

---

### 4. Clone the Skills Repo

```bash
cd ~ && git clone https://github.com/Bloomerang/quality-assistance-skills-wip ~/quality-assistance-skills
```

---

### 5. Get Your Jira API Token

1. Go to `https://id.atlassian.com/manage-profile/security/api-tokens`
2. Click **Create API token**, give it a name (e.g. "Claude Code"), and copy it somewhere safe

---

## Before You Start (One-Time Skill Setup)

You need a `jira-config.yaml` file with your Jira credentials. If you haven't done this yet:

1. Open Claude Code from your `quality-assistance-skills` folder:
   ```bash
   cd ~/quality-assistance-skills && claude
   ```
2. Type: `create a test plan for [any ticket number]`
3. Claude Code will detect that no config exists and walk you through creating it — you'll need:
   - Your Jira base URL (e.g. `https://bloomerang.atlassian.net`)
   - Your Jira email address
   - Your Jira API token — get one at `https://id.atlassian.com/manage-profile/security/api-tokens`

You only do this once. After that, the skill uses the saved config automatically.

---

## Every Day Use

### Step 1 — Open Claude Code in the skills folder

In your WSL terminal:
```bash
cd ~/quality-assistance-skills && claude
```

---

### Step 2 — Ask for a test plan

Type any of these (replace the ticket number with a real one):

```
create a test plan for BMA-1234
```
```
generate test cases for BMA-1234
```
```
what should we test for BMA-1234
```

Claude Code will pull the ticket details from Jira automatically.

---

### Step 3 — Optionally include a PR diff

If there's a pull request open for this ticket, Claude Code can review the code changes and factor them into the test plan.

When prompted, provide the PR number or URL. If there's no PR yet, just skip this step.

> Requires GitHub CLI (`gh`) to be authenticated. If you haven't set that up, skip this step for now.

---

### Step 4 — Review the generated test plan

Claude Code will generate a formatted test plan and show it to you. Review it and ask for changes if needed:

```
add negative test cases for the payment flow
```
```
remove the duplicate login steps
```
```
add an edge case for when the constituent has no saved payment method
```

Keep going back and forth until it looks right.

---

### Step 5 — Save it

Claude Code saves the test plan as a file in your project folder. It will tell you the file name and location when it's done.

---

### Step 6 — Upload to Xray (optional)

If you want to push the test cases directly into Jira/Xray, just say:

```
upload these tests to Xray
```

This hands off to the `xray-upload` skill. Make sure you've completed the Xray setup first (see the Xray Upload guide).

---

## Tips

- **You don't need the ticket open** — Claude Code fetches it directly from Jira
- **Be specific with feedback** — "add more edge cases" works, but "add edge cases for offline mode and expired sessions" gets better results
- **Review before uploading** — always read through the test plan before sending it to Xray; Claude Code is thorough but you know the product better
- **Works with feature descriptions too** — if there's no Jira ticket yet, you can paste a feature description directly and ask for test cases

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No config found" | Follow the one-time setup above |
| Can't fetch ticket | Check your Jira API token is valid and your email is correct in the config |
| PR diff not working | Make sure `gh auth login` has been run and you have repo access |
| Upload fails after generating | See the Xray Upload guide for credential setup |
