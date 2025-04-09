import os
from pathlib import Path
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class ProjectSummary(BaseModel):
    summary: str = Field(description="A concise, engaging summary of the project")
    key_features: list[str] = Field(description="List of 2-3 key features or highlights")
    tech_stack: list[str] = Field(description="Main technologies used in the project")

def read_readme(repo_path):
    readme_path = Path(repo_path) / "README.md"
    if not readme_path.exists():
        return None
    return readme_path.read_text()

def generate_summary_with_langchain(text):
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create output parser
    parser = PydanticOutputParser(pydantic_object=ProjectSummary)
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that creates detailed project summaries.
        Your task is to analyze the project description and create a comprehensive summary.
        {format_instructions}"""),
        ("user", "Please analyze this project description and create a summary:\n\n{text}")
    ])
    
    # Create the chain
    chain = prompt | llm | parser
    
    # Run the chain
    result = chain.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result

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

    # Generate summary using LangChain
    summary = generate_summary_with_langchain(readme_content)
    
    # Save the summary to a file
    output_path = Path(repo_path) / "project_summary_langchain.json"
    output_data = {
        "summary": summary.summary,
        "key_features": summary.key_features,
        "tech_stack": summary.tech_stack,
        "repo_name": Path(repo_path).name
    }
    
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"Summary saved to {output_path}")

if __name__ == "__main__":
    main() 