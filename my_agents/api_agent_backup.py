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
     Youare an API testing robot. Generate ONLY valid Python code for a pytest file using httpx that GETs /rockets/123asserts status 20 JSON has id field. Do NOT use the auth parameter in httpx.Client. Do NOT include any markdown formatting, comments, or explanations. Output ONLY valid Python code.
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

def generate_api_test():
    sticky = {"id": "API-S1", "risk": 0.1, "agent": "api"}
    code = Runner.run_sync(api_agent, str(sticky)).final_output
    code = clean_code(code)
    Path("tests/test_api.py").write_text(code)
    print("✅ tests/test_api.py created")