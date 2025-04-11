import os
import sys
import requests
from typing import Optional

def trigger_summarization(repo_name: str, github_token: Optional[str] = None) -> bool:
    """
    Trigger the summarization workflow for a repository.
    
    Args:
        repo_name: Name of the repository to summarize (format: owner/repo)
        github_token: GitHub personal access token with repo scope
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not github_token:
        github_token = os.getenv('PERSONAL_ACCESS_TOKEN') or os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("Error: GitHub token not provided. Set the PERSONAL_ACCESS_TOKEN or GITHUB_TOKEN environment variable.")
            return False
            
    try:
        owner, repo = repo_name.split('/')
    except ValueError:
        print("Error: Invalid repository format. Use 'owner/repo'.")
        return False
    
    # API endpoint for repository dispatch
    url = f"https://api.github.com/repos/{owner}/project-summarizer/dispatches"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }
    
    data = {
        "event_type": "summarize_repo",
        "client_payload": {
            "repository": repo_name,
            "repository_name": repo
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully triggered summarization for {repo_name}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error triggering summarization: {str(e)}")
        if response is not None and hasattr(response, "text"):
            print("Response body:", response.text)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trigger_summarization.py owner/repo")
        sys.exit(1)
        
    repo_name = sys.argv[1]
    success = trigger_summarization(repo_name)
    sys.exit(0 if success else 1)