# my_agents/api_agent.py
from pathlib import Path
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

groq_model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
)

api_agent = Agent(
    name="API-Agent",
    instructions=(
        "You are an API testing robot. "
        "Given sticky {'id':'API-S1'}, write a single pytest file using httpx "
        "that GET /rockets/123, asserts status 200 and JSON has 'id' field."
    ),
    model=groq_model
)

def generate_api_test():
    sticky = {"id": "API-S1", "risk": 0.1, "agent": "api"}
    code = Runner.run_sync(api_agent, str(sticky)).final_output
    Path("tests/test_api.py").write_text(code)
    print("✅ tests/test_api.py created")