import os
from pathlib import Path
from scripts.process_readme import main as process_openai
from scripts.process_readme_langchain import main as process_langchain

def setup_test_environment():
    # Set the test repository path
    test_repo_path = Path(__file__).parent / "test-repo"
    os.environ["GITHUB_WORKSPACE"] = str(test_repo_path)
    
    # Ensure OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set your OPENAI_API_KEY environment variable")
        print("You can do this by running:")
        print("export OPENAI_API_KEY='your-api-key'")
        return False
    return True

def main():
    if not setup_test_environment():
        return
    
    print("Testing OpenAI processor...")
    process_openai()
    
    print("\nTesting LangChain processor...")
    process_langchain()
    
    print("\nTest completed! Check the generated JSON files in the test-repo directory.")

if __name__ == "__main__":
    main() 