# my_agents/ui_agent.py
from pathlib import Path
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os, json

groq_model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
)

ui_agent = Agent(
    name="UI-Agent",
    instructions=(
        "You are a UI testing robot. "
        "Given a sticky note with id='UI-S1', write a single Playwright Python file "
        "that opens the rocket site, clicks the 'View Rocket' button, and asserts the title contains 'Rocket'."
    ),
    model=groq_model
)

def generate_ui_test():
    sticky = {"id": "UI-S1", "risk": 0.2, "agent": "ui"}
    code = Runner.run_sync(ui_agent, str(sticky)).final_output
    Path("tests/test_ui.py").write_text(code)
    print("✅ tests/test_ui.py created")