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
        "Given sticky {'id':'DATA-S1'}, write a pytest file that:\n"
        "1. Counts rows in source CSV `sales.csv`\n"
        "2. Counts rows in target warehouse table `rockets`\n"
        "3. Asserts counts match and row-hashes are identical."
    ),
    model=groq_model
)

def generate_data_test():
    sticky = {"id": "DATA-S1", "risk": 0.2, "agent": "data"}
    code = Runner.run_sync(data_agent, str(sticky)).final_output
    Path("tests/test_data.py").write_text(code)
    print("✅ tests/test_data.py created")