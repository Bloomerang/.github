const axios = require('axios');
const { context, getOctokit } = require('@actions/github');
const octokit = getOctokit(process.env.GITHUB_TOKEN);

async function run() {
  try {
    const prNumber = context.payload.pull_request.number;
    const prTitle = context.payload.pull_request.title;
    const prBody = context.payload.pull_request.body;

    const jiraTicketId = prTitle.match(/([A-Z]+-\d+)/)[0];
    const jiraTicketUrl = `${process.env.JIRA_BASE_URL}/browse/${jiraTicketId}`;

    console.log(`Jira Ticket ID: ${jiraTicketId}`);
    console.log(`Jira Ticket URL: ${jiraTicketUrl}`);

    const jiraResponse = await axios.get(`${process.env.JIRA_BASE_URL}/rest/api/2/issue/${jiraTicketId}`, {
      auth: {
        username: process.env.JIRA_USERNAME,
        password: process.env.JIRA_API_TOKEN
      }
    });

    const jiraDescription = jiraResponse.data.fields.description;

    const newPrBody = `## Description\n\n**Jira Ticket:** ${jiraTicketUrl}\n\n${jiraDescription}\n\n${prBody}`;

    await octokit.rest.pulls.update({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: prNumber,
      body: newPrBody
    });
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
}

run();