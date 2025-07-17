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
        "You are a UI testing robot. Given a sticky note with id='UI-S1', write ONLY the Python code for a Playwright Python file that opens http://mockapi:3000/rockets/123, clicks the 'View Rocket' button, and asserts the title contains 'Rocket'. Use from playwright.sync_api import sync_playwright for Playwright code. Always use headless=True when launching browser. Do NOT include any markdown formatting, comments, or explanations. Output ONLY valid Python code."
    ),
    model=groq_model
)

def clean_code(code):
    lines = code.splitlines()
    lines = [line for line in lines if not line.strip().startswith('```')]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)

def generate_ui_test():
    sticky = {"id": "UI-S1", "risk": 0.2, "agent": "ui"}
    code = Runner.run_sync(ui_agent, str(sticky)).final_output
    code = clean_code(code)
    Path("tests/test_ui.py").write_text(code)
    print("✅ tests/test_ui.py created")