# Text Analysis with AI Agent

This agent will ingest text provided by a user, after which it will classify the material, extract the main subjects that the material covers, and then provides a summary of the text.

## Setup
Create virtual environment 
```
python3 -m venv agent_env && source agent_env/bin/activate
```
Install dependencies
```
pip install langgraph langchain langchain-openai python-dotenv openai
```

Run the script
```
python3 agent.py <<< "User's text"
```