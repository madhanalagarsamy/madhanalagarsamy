// scripts/update-issue-count.mjs
// Fetches live "issues opened" stats for GITHUB_USERNAME from the GitHub
// Search API and:
//   1. writes /.github/badges/*.json  (consumed by shields.io "endpoint" badges)
//   2. rewrites the marker block inside README.md with a small live table
//
// Runs inside GitHub Actions (Node 20 has global fetch, no deps needed).

const USERNAME = process.env.GH_USERNAME;
const TOKEN = process.env.GH_TOKEN; // provided as secrets.GITHUB_TOKEN in the workflow

if (!USERNAME) {
  console.error("Missing GH_USERNAME env var");
  process.exit(1);
}

const headers = {
  "Accept": "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28",
  ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
};

async function searchCount(query) {
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=1`;
  const res = await fetch(url, { headers });
  if (!res.ok) {
    throw new Error(`GitHub API error ${res.status} for query "${query}": ${await res.text()}`);
  }
  const data = await res.json();
  return data.total_count ?? 0;
}

function badgeJson(label, message, color) {
  // shields.io "endpoint" schema: https://shields.io/badges/endpoint-badge
  return {
    schemaVersion: 1,
    label,
    message: String(message),
    color,
  };
}

async function main() {
  const totalOpened = await searchCount(`author:${USERNAME} type:issue`);
  const stillOpen = await searchCount(`author:${USERNAME} type:issue state:open`);
  const closed = await searchCount(`author:${USERNAME} type:issue state:closed`);
  const prsOpened = await searchCount(`author:${USERNAME} type:pr`);

  const fs = await import("node:fs/promises");

  await fs.mkdir(".github/badges", { recursive: true });
  await fs.writeFile(
    ".github/badges/issues-total.json",
    JSON.stringify(badgeJson("issues opened", totalOpened, "ff00cc"), null, 2)
  );
  await fs.writeFile(
    ".github/badges/issues-open.json",
    JSON.stringify(badgeJson("open", stillOpen, "00ffcc"), null, 2)
  );
  await fs.writeFile(
    ".github/badges/issues-closed.json",
    JSON.stringify(badgeJson("closed", closed, "ab00ff"), null, 2)
  );
  await fs.writeFile(
    ".github/badges/prs-total.json",
    JSON.stringify(badgeJson("PRs opened", prsOpened, "0a0512"), null, 2)
  );

  // ---- Update README.md live table between markers ----
  const readmePath = "README.md";
  let readme = await fs.readFile(readmePath, "utf8");

  const timestamp = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";

  const block = `<!--ISSUE_STATS_START-->
<table align="center">
  <tr>
    <td align="center"><b>Total Issues Opened</b><br/>${totalOpened}</td>
    <td align="center"><b>Currently Open</b><br/>${stillOpen}</td>
    <td align="center"><b>Closed</b><br/>${closed}</td>
    <td align="center"><b>PRs Opened</b><br/>${prsOpened}</td>
  </tr>
</table>
<p align="center"><sub>Last updated: ${timestamp}</sub></p>
<!--ISSUE_STATS_END-->`;

  const markerRegex = /<!--ISSUE_STATS_START-->[\s\S]*?<!--ISSUE_STATS_END-->/;

  if (markerRegex.test(readme)) {
    readme = readme.replace(markerRegex, block);
  } else {
    console.warn("Markers not found in README.md — appending block at the end instead.");
    readme += `\n\n${block}\n`;
  }

  await fs.writeFile(readmePath, readme);

  console.log({ totalOpened, stillOpen, closed, prsOpened });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
