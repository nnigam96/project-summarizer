import os
import openai
from pathlib import Path
import json

def read_readme(repo_path):
    readme_path = Path(repo_path) / "README.md"
    if not readme_path.exists():
        return None
    return readme_path.read_text()

def generate_summary(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates concise, engaging project summaries."},
            {"role": "user", "content": f"Please create a brief, engaging summary (2-3 sentences) of this project description:\n\n{text}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

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

    # Generate summary
    summary = generate_summary(readme_content)
    
    # Save the summary to a file
    output_path = Path(repo_path) / "project_summary.json"
    output_data = {
        "summary": summary,
        "repo_name": Path(repo_path).name
    }
    
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"Summary saved to {output_path}")

if __name__ == "__main__":
    main() 