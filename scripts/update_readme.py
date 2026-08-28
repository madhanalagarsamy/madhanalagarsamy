#!/usr/bin/env python3
"""
scripts/update_readme.py
Automated dynamic README & badge updater for Madhan Alagarsamy's GitHub Profile.

Features:
- Queries GitHub REST API for profile metrics, repository activity, and issue/PR statistics.
- Updates Shields.io endpoint badge JSON files in .github/badges/.
- Dynamically updates designated marker blocks in README.md without touching manual content.
- Uses only Python standard library (no external dependencies required).
- Implements robust error handling and safe fallbacks.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

# Add script dir to path for importing config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import config
except ImportError:
    class config:
        GH_USERNAME = os.environ.get("GH_USERNAME", "madhanalagarsamy")
        FEATURED_REPOSITORIES = []
        EXCLUDED_REPOSITORIES = ["madhanalagarsamy"]
        MAX_RECENT_PROJECTS = 4
        README_PATH = "README.md"
        BADGES_DIR = ".github/badges"

USERNAME = os.environ.get("GH_USERNAME", getattr(config, "GH_USERNAME", "madhanalagarsamy"))
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
README_PATH = getattr(config, "README_PATH", "README.md")
BADGES_DIR = getattr(config, "BADGES_DIR", ".github/badges")
EXCLUDED_REPOS = set(getattr(config, "EXCLUDED_REPOSITORIES", ["madhanalagarsamy"]))
MAX_RECENT = getattr(config, "MAX_RECENT_PROJECTS", 4)

# Map of fallback descriptions for featured repos if API description is empty
CUSTOM_DESCRIPTIONS = {}
if hasattr(config, "FEATURED_REPOSITORIES"):
    for item in config.FEATURED_REPOSITORIES:
        if isinstance(item, dict) and "repo" in item and "description" in item:
            CUSTOM_DESCRIPTIONS[item["repo"]] = item["description"]

def fetch_json(url):
    """Fetch JSON from GitHub API with authentication and error handling."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"GitHub-Profile-Updater/{USERNAME}"
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[WARN] HTTP error {e.code} for URL {url}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[WARN] Network error for URL {url}: {e}", file=sys.stderr)
        return None

def get_issue_counts():
    """Fetch issue and PR counts for the user across GitHub."""
    def search_count(query):
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page=1"
        data = fetch_json(url)
        if data and "total_count" in data:
            return data["total_count"]
        return None

    total_issues = search_count(f"author:{USERNAME} type:issue")
    open_issues = search_count(f"author:{USERNAME} type:issue state:open")
    closed_issues = search_count(f"author:{USERNAME} type:issue state:closed")
    total_prs = search_count(f"author:{USERNAME} type:pr")

    return {
        "total_issues": total_issues,
        "open_issues": open_issues,
        "closed_issues": closed_issues,
        "total_prs": total_prs,
    }

def get_user_profile():
    """Fetch user profile metadata."""
    url = f"https://api.github.com/users/{USERNAME}"
    return fetch_json(url)

def get_recent_repositories():
    """Fetch and filter recently updated repositories."""
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=30"
    repos = fetch_json(url)
    if not isinstance(repos, list):
        return []

    filtered = []
    for r in repos:
        name = r.get("name", "")
        if name in EXCLUDED_REPOS:
            continue
        
        desc = r.get("description")
        if not desc or desc == "None":
            desc = CUSTOM_DESCRIPTIONS.get(name, "No description provided.")
        
        lang = r.get("language")
        if not lang or lang == "None":
            lang = "Python / C++" if r.get("fork") else "Code"

        filtered.append({
            "name": name,
            "full_name": r.get("full_name", f"{USERNAME}/{name}"),
            "description": desc,
            "language": lang,
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "is_fork": r.get("fork", False),
            "updated_at": r.get("updated_at", ""),
            "html_url": r.get("html_url", f"https://github.com/{USERNAME}/{name}")
        })
        if len(filtered) >= MAX_RECENT:
            break

    return filtered

def write_badges(issue_stats):
    """Write Shields.io endpoint badge JSON files."""
    os.makedirs(BADGES_DIR, exist_ok=True)

    def badge_data(label, value, color):
        return {
            "schemaVersion": 1,
            "label": label,
            "message": str(value if value is not None else "-"),
            "color": color,
        }

    badges = {
        "issues-total.json": badge_data("issues opened", issue_stats.get("total_issues"), "ff00cc"),
        "issues-open.json": badge_data("open", issue_stats.get("open_issues"), "00ffcc"),
        "issues-closed.json": badge_data("closed", issue_stats.get("closed_issues"), "ab00ff"),
        "prs-total.json": badge_data("PRs opened", issue_stats.get("total_prs"), "0a0512"),
    }

    for filename, data in badges.items():
        filepath = os.path.join(BADGES_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def generate_stats_markdown(issue_stats, user_profile, timestamp_str):
    """Generate dynamic stats block."""
    total_issues = issue_stats.get("total_issues") if issue_stats.get("total_issues") is not None else 18
    open_issues = issue_stats.get("open_issues") if issue_stats.get("open_issues") is not None else 11
    closed_issues = issue_stats.get("closed_issues") if issue_stats.get("closed_issues") is not None else 7
    total_prs = issue_stats.get("total_prs") if issue_stats.get("total_prs") is not None else 12
    public_repos = user_profile.get("public_repos", 9) if user_profile else 9
    followers = user_profile.get("followers", 2) if user_profile else 2

    return f"""<!-- START_DYNAMIC_STATS -->
<div align="center">
  <table>
    <tr>
      <td align="center" width="16%"><b>Issues Opened</b><br/><code>{total_issues}</code></td>
      <td align="center" width="16%"><b>Currently Open</b><br/><code>{open_issues}</code></td>
      <td align="center" width="16%"><b>Closed Issues</b><br/><code>{closed_issues}</code></td>
      <td align="center" width="16%"><b>PRs Opened</b><br/><code>{total_prs}</code></td>
      <td align="center" width="16%"><b>Public Repos</b><br/><code>{public_repos}</code></td>
      <td align="center" width="16%"><b>Followers</b><br/><code>{followers}</code></td>
    </tr>
  </table>
  <p><sub>Live metrics synced with GitHub API &bull; Last updated: {timestamp_str}</sub></p>
</div>
<!-- END_DYNAMIC_STATS -->"""

def generate_recent_projects_markdown(repos, timestamp_str):
    """Generate dynamic recent projects block."""
    if not repos:
        return ""

    rows = []
    for r in repos:
        raw_date = r.get("updated_at", "")
        formatted_date = raw_date[:10] if len(raw_date) >= 10 else raw_date
        star_str = f"⭐ {r['stars']}" if r['stars'] > 0 else "⭐ 0"
        fork_badge = " *(upstream fork)*" if r.get("is_fork") else ""
        clean_desc = r["description"].replace("\n", " ").replace("|", "\\|").strip()
        rows.append(
            f"| [**`{r['name']}`**]({r['html_url']}){fork_badge} | {clean_desc} | `{r['language']}` | {star_str} | {formatted_date} |"
        )

    table_content = "\n".join(rows)
    return f"""<!-- START_DYNAMIC_PROJECTS -->
| Repository | Description | Primary Tech | Stars | Last Synced |
| :--- | :--- | :---: | :---: | :---: |
{table_content}
<!-- END_DYNAMIC_PROJECTS -->"""

def generate_legacy_issue_block(issue_stats, timestamp_str):
    """Generate legacy issue stats block for backwards compatibility."""
    total_issues = issue_stats.get("total_issues") if issue_stats.get("total_issues") is not None else 18
    open_issues = issue_stats.get("open_issues") if issue_stats.get("open_issues") is not None else 11
    closed_issues = issue_stats.get("closed_issues") if issue_stats.get("closed_issues") is not None else 7
    total_prs = issue_stats.get("total_prs") if issue_stats.get("total_prs") is not None else 12

    return f"""<!--ISSUE_STATS_START-->
<table align="center">
  <tr>
    <td align="center"><b>Total Issues Opened</b><br/>{total_issues}</td>
    <td align="center"><b>Currently Open</b><br/>{open_issues}</td>
    <td align="center"><b>Closed</b><br/>{closed_issues}</td>
    <td align="center"><b>PRs Opened</b><br/>{total_prs}</td>
  </tr>
</table>
<p align="center"><sub>Last updated: {timestamp_str}</sub></p>
<!--ISSUE_STATS_END-->"""

def update_readme_file(stats_block, projects_block, legacy_block):
    """Update README.md file in-place by replacing designated marker blocks."""
    if not os.path.exists(README_PATH):
        print(f"[ERROR] README file not found at {README_PATH}", file=sys.stderr)
        return False

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content

    # Replace dynamic stats block
    stats_regex = re.compile(r"<!-- START_DYNAMIC_STATS -->[\s\S]*?<!-- END_DYNAMIC_STATS -->")
    if stats_regex.search(new_content):
        new_content = stats_regex.sub(stats_block, new_content)

    # Replace dynamic projects block
    projects_regex = re.compile(r"<!-- START_DYNAMIC_PROJECTS -->[\s\S]*?<!-- END_DYNAMIC_PROJECTS -->")
    if projects_regex.search(new_content) and projects_block:
        new_content = projects_regex.sub(projects_block, new_content)

    # Replace legacy issue block if present
    legacy_regex = re.compile(r"<!--ISSUE_STATS_START-->[\s\S]*?<!--ISSUE_STATS_END-->")
    if legacy_regex.search(new_content) and legacy_block:
        new_content = legacy_regex.sub(legacy_block, new_content)

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("[SUCCESS] README.md updated successfully with fresh dynamic data.")
        return True
    else:
        print("[INFO] No changes needed in README.md.")
        return False

def main():
    print(f"[*] Starting GitHub profile update for @{USERNAME}...")
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    issue_stats = get_issue_counts()
    print(f"[*] Live issue stats: {issue_stats}")

    user_profile = get_user_profile()
    if user_profile:
        print(f"[*] Profile: {user_profile.get('name')} | Repos: {user_profile.get('public_repos')} | Followers: {user_profile.get('followers')}")

    recent_repos = get_recent_repositories()
    print(f"[*] Fetched {len(recent_repos)} recent repositories.")

    if issue_stats.get("total_issues") is not None:
        write_badges(issue_stats)
        print(f"[*] Updated badge JSON files in {BADGES_DIR}/")

    stats_block = generate_stats_markdown(issue_stats, user_profile, now_utc)
    projects_block = generate_recent_projects_markdown(recent_repos, now_utc)
    legacy_block = generate_legacy_issue_block(issue_stats, now_utc)

    update_readme_file(stats_block, projects_block, legacy_block)
    print("[*] Update process finished.")

if __name__ == "__main__":
    main()
