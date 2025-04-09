import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from huggingface_hub import InferenceClient

def read_readme(repo_path: str) -> str:
    """Read the README file from the specified repository path."""
    readme_path = Path(repo_path) / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError(f"README.md not found in {repo_path}")
    return readme_path.read_text(encoding="utf-8")

def extract_tech_stack(text: str) -> List[str]:
    """Extract technology stack from the README text."""
    tech_keywords = [
        "python", "pytorch", "tensorflow", "flask", "django", "react", "vue",
        "node", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "docker", "kubernetes", "aws", "azure", "gcp", "postgresql", "mysql",
        "mongodb", "redis", "nginx", "apache"
    ]
    
    found_tech = []
    for keyword in tech_keywords:
        if keyword.lower() in text.lower():
            found_tech.append(keyword)
    return found_tech

def extract_features(text: str) -> List[str]:
    """Extract bullet points from the README as features."""
    features = []
    lines = text.split("\n")
    for line in lines:
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            feature = line.strip()[2:].strip()
            if feature:
                features.append(feature)
    return features[:3]  # Return top 3 features

def generate_summary_with_llm(text: str, api_token: Optional[str] = None) -> Dict:
    """Generate summary using Hugging Face's Inference API with a free LLM."""
    try:
        # Initialize the Inference client
        client = InferenceClient(model="google/flan-t5-small", token=api_token)
        
        # Create a prompt for summarization
        prompt = f"""Please summarize the following project description in 2-3 sentences, focusing on its main purpose and key features:

{text}

Summary:"""
        
        # Generate summary
        summary = client.text_generation(
            prompt,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        
        # Extract tech stack and features
        tech_stack = extract_tech_stack(text)
        features = extract_features(text)
        
        return {
            "summary": summary.strip(),
            "tech_stack": tech_stack,
            "features": features
        }
        
    except Exception as e:
        print(f"Error during LLM summarization: {str(e)}")
        # Fallback to simple text extraction
        return {
            "summary": text[:200] + "...",
            "tech_stack": extract_tech_stack(text),
            "features": extract_features(text)
        }

def main():
    """Main function to process README and generate summary."""
    repo_path = os.getenv("GITHUB_WORKSPACE", ".")
    api_token = os.getenv("HF_API_TOKEN")
    
    try:
        # Read README
        readme_text = read_readme(repo_path)
        
        # Generate summary
        summary_data = generate_summary_with_llm(readme_text, api_token)
        
        # Save summary
        output_path = Path(repo_path) / "project_summary_llm.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2)
            
        print(f"Summary saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 