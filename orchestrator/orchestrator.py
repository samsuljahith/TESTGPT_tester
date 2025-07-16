# quick_orchestrator.py
import os, json, yaml
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from my_agents.planning_agent import planning_agent

# Groq-backed Mistral model
groq_model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
)

# ------------- Agents -------------
orchestrator = Agent(
    name="Orchestrator",
    instructions="You are the entry point. Forward raw spec to PlanningAgent.",
    model=groq_model
)



# ------------- Run -------------
if __name__ == "__main__":
    import re
    import os
    spec = yaml.safe_load(open("sample.yaml"))
    raw = yaml.dump(spec)
    plan = Runner.run_sync(planning_agent, raw).final_output
    print("📋 PlanningAgent output:\n", plan)

    # Try to extract JSON code block first
    match = re.search(r"```json\s*(.*?)\s*```", plan, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Fallback: try to parse the whole output
        json_str = plan.strip()
    try:
        os.makedirs("tests", exist_ok=True)
        json.dump(json.loads(json_str), open("tests/backlog.json", "w"), indent=2)
    except Exception as e:
        print("Failed to parse JSON from PlanningAgent output:", e)