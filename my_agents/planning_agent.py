import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

# Set up the Groq-backed Mistral model
groq_model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
)

# Define the PlanningAgent
planning_agent = Agent(
    name="PlanningAgent",
    instructions=(
        "You are a planning robot. "
        "Read the YAML spec and output ONLY a JSON list with exactly 4 items. "
        "Each item must have: id (string), risk (number 0-1), agent (one of: api, ui, data, nfr). "
        "Do NOT add extra keys. "
        "Example:\n"
        '[{"id":"API-S1","risk":0.4,"agent":"api"},'
        '{"id":"UI-S1","risk":0.6,"agent":"ui"},'
        '{"id":"DATA-S1","risk":0.3,"agent":"data"},'
        '{"id":"NFR-S1","risk":0.5,"agent":"nfr"}]'
    ),
    model=groq_model
)