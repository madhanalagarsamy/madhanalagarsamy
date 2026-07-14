
import os
import re
import urllib.request
import json
import ssl

def get_issues_count(username):
    url = f"https://api.github.com/search/issues?q=author:{username}+type:issue"
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    )
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response:
            data = json.loads(response.read().decode())
            return data.get("total_count", 0)
    except Exception as e:
        print(f"Error fetching issues count: {e}")
        return 0

def main():
    username = os.getenv("GITHUB_REPOSITORY_OWNER")
    if not username:
        username = "madhanalagarsamy"
    
    count = get_issues_count(username)
    print(f"Found {count} issues opened by {username}")
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r"(<!-- ISSUES_COUNT_START -->)(.*?)(<!-- ISSUES_COUNT_END -->)"
    badge_url = f"https://img.shields.io/badge/Issues%20Opened-{count}-00ffcc?style=for-the-badge"
    replacement = f"\\1<img src=\"{badge_url}\" alt=\"Issues Opened\" />\\3"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md has been successfully updated with the current issue count.")

if __name__ == "__main__":
    main()
