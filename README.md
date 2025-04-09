# Project Summarizer

This GitHub Action automatically generates summaries of your GitHub projects whenever their README.md files are updated. It uses OpenAI's GPT model to create concise, engaging summaries that can be used to showcase your projects.

## Features

- Automatically triggers when README.md files are updated
- Generates engaging project summaries using GPT-3.5
- Provides two processing methods:
  - Direct OpenAI API integration
  - LangChain-based processing with structured output
- Saves summaries in JSON format for easy integration
- Easy to customize and extend

## Setup

1. Fork or clone this repository
2. Add your OpenAI API key as a repository secret:
   - Go to your repository settings
   - Navigate to Secrets and Variables > Actions
   - Add a new secret named `OPENAI_API_KEY` with your OpenAI API key

3. Configure the workflow:
   - The workflow is configured to run on pushes to the main branch
   - It looks for changes in README.md files
   - Customize the workflow in `.github/workflows/update-projects.yml` as needed

## How it Works

1. When you push changes to a README.md file, the GitHub Action is triggered
2. The action checks out your repository and sets up Python
3. It processes the README.md file using two methods:

   a) **OpenAI Direct Method**:
   - Simple, direct API call to OpenAI
   - Generates a basic summary
   - Outputs to `project_summary.json`

   b) **LangChain Method**:
   - More sophisticated processing
   - Extracts summary, key features, and tech stack
   - Outputs to `project_summary_langchain.json`

4. The summaries are saved in JSON format for easy integration with your website or documentation

## Output Formats

OpenAI version (`project_summary.json`):
```json
{
  "summary": "Your project summary here...",
  "repo_name": "repository-name"
}
```

LangChain version (`project_summary_langchain.json`):
```json
{
  "summary": "Your project summary here...",
  "key_features": ["Feature 1", "Feature 2", "Feature 3"],
  "tech_stack": ["Technology 1", "Technology 2"],
  "repo_name": "repository-name"
}
```

## Testing

To test the summarizer locally:

```bash
# 1. Set up your OpenAI API key
export OPENAI_API_KEY='your-api-key'

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the test script
python test.py
```

## Customization

You can customize the summary generation by:
- Modifying the prompts in `scripts/process_readme.py`
- Adjusting the Pydantic model in `scripts/process_readme_langchain.py`
- Changing the output format
- Adding new processing steps

## License

MIT License 