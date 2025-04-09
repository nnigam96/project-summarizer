import os
import json
from pathlib import Path
import requests

def read_readme(repo_path):
    readme_path = Path(repo_path) / "README.md"
    if not readme_path.exists():
        return None
    return readme_path.read_text()

def generate_summary_with_ollama(text):
    # Ollama API endpoint (assuming it's running locally)
    url = "http://localhost:11434/api/generate"
    
    # Prepare the prompt
    prompt = f"""Please analyze this project description and create a comprehensive summary.
    Include the following in your response:
    1. A brief, engaging summary (2-3 sentences)
    2. 2-3 key features or highlights
    3. Main technologies used
    
    Project Description:
    {text}
    
    Please format your response as a JSON object with these fields:
    - summary: string
    - key_features: array of strings
    - tech_stack: array of strings
    """
    
    # Prepare the request
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    # Make the request
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    # Parse the response
    result = response.json()
    return json.loads(result["response"])

def main():
    # Get the repository path from environment variable
    repo_path = os.getenv("GITHUB_WORKSPACE")
    if not repo_path:
        print("Error: GITHUB_WORKSPACE environment variable not set")
        return

    # Read the README
    readme_content = read_readme(repo_path)
    if not readme_content:
        print("Error: README.md not found")
        return

    # Generate summary using Ollama
    summary = generate_summary_with_ollama(readme_content)
    
    # Save the summary to a file
    output_path = Path(repo_path) / "project_summary_ollama.json"
    output_data = {
        "summary": summary["summary"],
        "key_features": summary["key_features"],
        "tech_stack": summary["tech_stack"],
        "repo_name": Path(repo_path).name
    }
    
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"Summary saved to {output_path}")

if __name__ == "__main__":
    main() 