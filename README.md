# TESTGPT Tester — Multi-Agent QA Orchestration Framework

An agentic QA framework that reads a YAML spec, breaks it into a prioritised backlog, and routes test tasks to specialised agents (API, UI, Data, NFR). Built on the OpenAI Agents SDK (Groq-backed LLaMA 3.1), with a mock server, Locust load tests, and pytest suites.

## Architecture

```
sample.yaml (spec)
  → PlanningAgent   — parses spec, outputs JSON backlog [{id, risk, agent}]
  → Orchestrator    — routes tasks by agent type
      ├─ ApiAgent   — tests REST endpoints against fake_api/
      ├─ UIAgent    — UI interaction tests
      ├─ DataAgent  — data quality / schema validation
      └─ NfrAgent   — non-functional requirements (perf, security)
```

## Components

| Path | Description |
|------|-------------|
| `sample.yaml` | Test specification input |
| `orchestrator/orchestrator.py` | Entry point — runs planning → routing |
| `my_agents/planning_agent.py` | LLM agent that converts YAML → JSON task backlog |
| `my_agents/api_agent.py` | REST API test agent |
| `my_agents/ui_agent.py` | UI test agent |
| `my_agents/data_agent.py` | Data validation agent |
| `my_agents/nfr_agent.py` | Performance/security agent |
| `mock_server.py` | Local mock API server (served from `fake_api/`) |
| `tests/locustfile.py` | Locust load test config |
| `tests/test_api.py` | pytest API tests |
| `TESTGPT_demo.ipynb` | Notebook walkthrough |

## Setup

```bash
pip install openai-agents langchain-groq pyyaml pytest locust python-dotenv

# .env
GROQ_API_KEY=your_key
```

### Run the mock server

```bash
python mock_server.py
```

### Run the orchestrator

```bash
python orchestrator/orchestrator.py
# Outputs: tests/backlog.json
```

### Run tests

```bash
pytest tests/
locust -f tests/locustfile.py
```

## Tech Stack

- **Agents SDK** — OpenAI Agents (Groq-compatible via OpenAI base URL)
- **LLM** — Groq `llama-3.1-8b-instant`
- **Load testing** — Locust
- **Unit testing** — pytest
- **CI** — GitHub Actions (`.github/workflows/ci.yml`)
