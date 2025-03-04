# Text Analysis with AI Agent

This agent will ingest text provided by a user, after which it will classify the material, extract the main subjects that the material covers, and then provides a summary of the text.

## Setup

1. Create virtual environment

```
python3 -m venv agent_env && source agent_env/bin/activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Add your OpenAI API key to .env file


4. Run the script

```
python3 agent.py <<< "Your text"
```
