from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from google.adk.tools import google_search

from .prompts.root_agent_prompt import ROOT_AGENT_PROMPT
from .tools.youtube_transcript import get_youtube_transcript

import os
from dotenv import load_dotenv
load_dotenv()

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

model = Gemini(
        model="gemini-2.0-flash-lite",
        retry_options=retry_config
    )

ollama_model=LiteLlm(model="ollama_chat/gemma4:e2b")


def add(a:int, b:int) -> dict:
    """ Adding two numbers """
    return {"result":a+b}

root_agent=LlmAgent(
    name="second_agent",
    # model=ollama_model,
    model=model,
    instruction="You are a helpful math assistant",
    description=ROOT_AGENT_PROMPT,
    output_key="second_agent_response",
    tools=[get_youtube_transcript]

)

