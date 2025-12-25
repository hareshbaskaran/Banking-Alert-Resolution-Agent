# Banking-Alert-Resolution-Agent
Agentic Alert Resolution System (AARS) to automatically investigate and resolve pre-generated banking transaction monitoring alerts.

## Technical Stack
- Python - Programming Language (3.11 / 3.8 + supported)
- Langgraph - Orchestrate Statefull Multi Agentic Workflow
- Langchain - Incorporate LLM Model, Tool Intefraces, Output Parsers for Agents
- Pydantic - Schematic Validation for Mock Databases, Agent Outputs and Type Safety
- Gemini - LLM Inference with Gemini Flash 2.5 Model with Langchain Interface

## Setup Configuration
- Create Python Virtual Environment (Python 3.8 +)
- Run """pip install -r requirements.txt""" command in terminal
- execute main.py file to execute all scenarios listed or create alert structure in CLI - """python -m app.main"""

## Required Project Setup
- Gemini API Key is a required credential 
- Add the Gemini API key into a .env file under GOOGLE_API_KEY namespace
- note : PAID API KEY IS MUST AS FREE API KEY CANNOT HANDLE MULTIPLE RPM

## AGENT ARCHITECTURE : docs/ARCHITECTURE.md





