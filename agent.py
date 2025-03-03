import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END #StateGraph = create the agent's structure
from langchain.prompts import PromptTemplate #PromptTemplate and ChatOpenAI provide tools to interact with AI models
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import openai
from dotenv import load_dotenv
import sys


# Load environment variables
load_dotenv()

# Create agent's working memory to keep track of information
class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    summary: str

# Initialize the agent's components
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
workflow = StateGraph(State)

# Define the agent's structure
# Provide instructions to the model to classify the text into one of the listed categories

def classification_node(state: State):
    ''' Classify the text into one of the categories: News, Blog, Research, or Other '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText:{text}\n\nCategory:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke([message]).content.strip()
    return {"classification": classification}


# Agent should remember important entities in the text
def entity_extraction_node(state: State):
    ''' Extract entities from the text '''
    # Extract entities from the text
    prompt = PromptTemplate(
        # Define the input variables for the prompt
        input_variables=["text"],
        # Provide instructions to the model to extract entities from the text
        template="Extract the entities from the following text. \
        Provide the result as a comma-separated list.\n\nText:{text}\n\nEntities:"
    )
    # Create a message with the prompt
    message = HumanMessage(content=prompt.format(text=state["text"]))
    # Invoke the model to extract entities
    entities = llm.invoke([message]).content.strip().split(", ")#split("\n")
    return {"entities": entities}


# Agent should summarize the text
def summarization_node(state: State):
    ''' Summarize the text '''
    prompt = PromptTemplate(
        # Define the input variables for the prompt
        input_variables=["text"],
        # Provide instructions to the model to summarize the text
        template="Summarize the following text.\n\nText:{text}\n\nSummary:"
    )
    # Create a message with the prompt
    message = HumanMessage(content=prompt.format(text=state["text"]))
    # Invoke the model to summarize the text
    summary = llm.invoke([message]).content.strip()
    return {"summary": summary}


def nodes_edges():
    # The functions defined above will be added as nodes to the graph
    workflow.add_node("classification_node", classification_node)
    workflow.add_node("entity_extraction", entity_extraction_node)
    workflow.add_node("summarization", summarization_node)

    # Add edges to the graph
    # Define the flow of information between the nodes
    workflow.set_entry_point("classification_node") # Set the entry point of the graph
    workflow.add_edge("classification_node", "entity_extraction")
    workflow.add_edge("entity_extraction", "summarization")
    workflow.add_edge("summarization", END)

    # Compile the graph
    app = workflow.compile()
    return app

def main():
    classification_node
    entity_extraction_node
    summarization_node
        
    local_app = nodes_edges()
    return local_app
    

try:

    if len(sys.argv) > 1:
        users_text = sys.argv[1]
    else:
       users_text = input("Enter some text:")

    app = main()

    state_input = {"text": users_text}
    result = app.invoke(state_input)

    print("Classification:", result["classification"])
    print("\nEntities:", result["entities"])
    print("\nSummary:", result["summary"])
    

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