# my_agents/data_agent.py
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

data_agent = Agent(
    name="Data-Agent",
    instructions=(
        "You are a data testing robot. "
        "Given sticky {'id':'DATA-S1'}, write ONLY the Python code for a pytest file that: 1. Counts rows in source CSV `sales.csv` 2. Counts rows in target warehouse table `rockets` 3. Asserts counts match and row-hashes are identical. Do NOT include any markdown formatting, comments, or explanations. Output ONLY valid Python code."
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

def generate_data_test():
    sticky = {"id": "DATA-S1", "risk": 0.2, "agent": "data"}
    code = Runner.run_sync(data_agent, str(sticky)).final_output
    code = clean_code(code)
    Path("tests/test_data.py").write_text(code)
    print("✅ tests/test_data.py created")