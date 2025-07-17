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
        "You are a load-test robot. Given sticky {'id':'NFR-S1'}, write ONLY the Python code for a Locustfile that: - hits GET /rockets/123 on host http://localhost:4000 - runs 1 000 concurrent users - asserts p95 latency < 300 ms. Do NOT include any markdown formatting, comments, or explanations. Output ONLY valid Python code."
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

def generate_nfr_test():
    sticky = {"id": "NFR-S1", "risk": 0.6, "agent": "nfr"}
    code = Runner.run_sync(nfr_agent, str(sticky)).final_output
    code = clean_code(code)
    Path("tests/locustfile.py").write_text(code)
    print("✅ tests/locustfile.py created")