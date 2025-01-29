import requests
import pdfkit
import os

# GitHub username
GITHUB_USERNAME = "your_github_username"

# Fetch repositories from GitHub API
url = f"https://github.com/rbhardwaj2186/github-portfolio.git"
response = requests.get(url)
repos = response.json()

# HTML Template for PDF
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

# Add repositories to the HTML content
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

print("Portfolio PDF generated successfully!")
