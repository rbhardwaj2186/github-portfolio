import requests
import pdfkit
import os

# GitHub username
GITHUB_USERNAME = "rbhardwaj2186"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("PDFPORTFOLIO")  # Fetch from GitHub Actions Secrets

# GitHub API URL
url = f"https://api.github.com/users/rbhardwaj2186/repos"  # ✅ Correct API URL

# Use authentication to avoid rate limits
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# Fetch repositories from GitHub API
response = requests.get(url, headers=headers)

# ✅ Check if the request was successful
if response.status_code != 200:
    print(f"❌ GitHub API request failed! Status code: {response.status_code}")
    print(f"🔹 Response content: {response.text}")
    exit(1)

# ✅ Try to parse JSON safely
try:
    repos = response.json()
except requests.exceptions.JSONDecodeError:
    print("❌ Failed to decode JSON response. Possible empty response or API issue.")
    print(f"🔹 Response content: {response.text}")
    exit(1)

# ✅ Check if we actually got repositories
if not isinstance(repos, list):
    print("❌ Unexpected API response format. Exiting.")
    print(f"🔹 Response content: {response.text}")
    exit(1)

# Generate PDF content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GitHub Portfolio</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { text-align: center; }
        .repo { margin-bottom: 20px; padding: 10px; border-bottom: 1px solid #ddd; }
        .repo h2 { margin: 0; }
        .repo p { margin: 5px 0; }
        a { color: #0366d6; text-decoration: none; }
    </style>
</head>
<body>
    <h1>GitHub Portfolio</h1>
"""

for repo in repos:
    html_content += f"""
    <div class="repo">
        <h2><a href="{repo['html_url']}">{repo['name']}</a></h2>
        <p><strong>Description:</strong> {repo.get('description', 'No description provided')}</p>
        <p><strong>Language:</strong> {repo.get('language', 'Unknown')}</p>
        <p><strong>Last Updated:</strong> {repo['updated_at'][:10]}</p>
    </div>
    """

html_content += "</body></html>"

# Save HTML file
with open("portfolio.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Convert HTML to PDF
pdfkit.from_file("portfolio.html", "GitHub_Portfolio.pdf")

print("✅ Portfolio PDF generated successfully!")
