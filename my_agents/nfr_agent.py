# my_agents/nfr_agent.py
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

nfr_agent = Agent(
    name="NFR-Agent",
    instructions=(
        "You are a load-test robot. "
        "Given sticky {'id':'NFR-S1'}, write a Locustfile that:\n"
        "- hits GET /rockets/123\n"
        "- runs 1 000 concurrent users\n"
        "- asserts p95 latency < 300 ms."
    ),
    model=groq_model
)

def generate_nfr_test():
    sticky = {"id": "NFR-S1", "risk": 0.6, "agent": "nfr"}
    code = Runner.run_sync(nfr_agent, str(sticky)).final_output
    Path("tests/locustfile.py").write_text(code)
    print("✅ tests/locustfile.py created")