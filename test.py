# Make sure API key works

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import openai

try:
    # Load environment variables
    load_dotenv()

    # Initialize the ChatOpenAI instance
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Test the setup
    response = llm.invoke("Hello! Are you working?")

    print(response.content)
    print(response.status_code)
    print(response.headers)
    print(response.json())
    print(response.text)
    print(response.request)
    print(response.url)
    print(response.links)
    print(response.encoding)
    print(response.elapsed)
    print(response.raw)
    print(response.reason)
    print(response.cookies)
    print(response.history)
    print(response.is_redirect)
except openai.RateLimitError as e:
    print(f"Unexpected {e=}, {type(e)=}")
except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"Failed to connect to OpenAI API: {e}")
except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"OpenAI API request exceeded rate limit: {e}")
except openai.OpenAIError as e:
  print(f"The api key is missing: {e}")
