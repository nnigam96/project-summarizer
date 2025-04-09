import os
import json
from pathlib import Path
from transformers import pipeline

def read_readme(repo_path):
    readme_path = Path(repo_path) / "README.md"
    if not readme_path.exists():
        return None
    return readme_path.read_text()

def extract_tech_stack(text):
    # Simple regex-based extraction of tech stack
    tech_stack = []
    tech_keywords = ["React", "Node.js", "TypeScript", "JavaScript", "Python", 
                    "Java", "Go", "Rust", "MongoDB", "PostgreSQL", "MySQL",
                    "Docker", "Kubernetes", "AWS", "Azure", "GCP"]
    
    for tech in tech_keywords:
        if tech.lower() in text.lower():
            tech_stack.append(tech)
    return tech_stack

def extract_features(text):
    # Extract bullet points as features
    features = []
    lines = text.split('\n')
    for line in lines:
        if line.strip().startswith('-'):
            feature = line.strip('- ').strip()
            features.append(feature)
    return features[:3]  # Return top 3 features

def generate_summary_with_hf(text):
    try:
        # Initialize the summarization pipeline with a smaller model
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        
        # Generate summary
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        
        # Extract additional information
        tech_stack = extract_tech_stack(text)
        features = extract_features(text)
        
        return {
            "summary": summary[0]['summary_text'],
            "key_features": features,
            "tech_stack": tech_stack
        }
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        # Fallback to simple extraction if summarization fails
        return {
            "summary": text[:200] + "...",  # First 200 characters as summary
            "key_features": extract_features(text),
            "tech_stack": extract_tech_stack(text)
        }

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

    # Generate summary using Hugging Face
    summary = generate_summary_with_hf(readme_content)
    
    # Save the summary to a file
    output_path = Path(repo_path) / "project_summary_hf.json"
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