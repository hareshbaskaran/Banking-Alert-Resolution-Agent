# Agentic Alert Resolution System — Orchestration Overview

## High-Level Philosophy
This system follows **deterministic agent orchestration** designed for regulated AML environments.

Core principles:
- LLMs reason only about **what information is missing**, not outcomes
- All metrics are **computed from data**, never inferred or hallucinated
- SOPs are **rule-based and enforced strictly**
- Each agent has a **single, non-overlapping responsibility**

No agent performs another agent’s job.

---

## Agent Roles & Responsibilities

### 1. Orchestrator (Hub)
**Purpose:** Control investigation flow

Responsibilities:
- Reads the scenario definition
- Identifies required findings for the scenario
- Compares required findings with current state
- Routes execution to the correct specialist agent

Constraints:
- NEVER computes metrics
- NEVER applies SOP logic
- NEVER makes risk decisions

Reasoning type:
- Gap-based (what is missing vs what is available)

---

### 2. Investigator Agent
**Purpose:** Transaction analysis

Responsibilities:
- Works ONLY on transactional data
- Computes quantitative metrics defined by the scenario:
  - Velocity spikes
  - Aggregate amounts
  - Geographic diversity
  - Temporal patterns

Constraints:
- No profile/KYC access
- No SOP interpretation
- No decision-making

Output:
- Deterministic, auditable findings derived strictly from transaction data

---

### 3. Context Gatherer Agent
**Purpose:** Profile & KYC analysis

Responsibilities:
- Works ONLY on customer profile/KYC data
- Extracts categorical attributes:
  - Occupation category
  - KYC risk level
  - Sanctions flag
  - Jurisdiction

Constraints:
- No transaction analysis
- No SOP logic
- No risk scoring

Output:
- Clean, validated contextual facts

---

### 4. Adjudicator
**Purpose:** Policy enforcement

Responsibilities:
- Applies SOP rules verbatim
- Consumes validated findings from prior agents
- Produces final outputs:
  - Decision
  - Risk level
  - Rationale (rule-based)

Constraints:
- No data computation
- No information gathering
- No tool execution

The Adjudicator behaves like a **policy engine**, not an exploratory AI.

---

### 5. Action Execution Module (AEM)
**Purpose:** Execute post-decision actions

Responsibilities:
- Reads adjudication result
- Triggers the appropriate simulated tool
- Prints clear, auditable console output

Constraints:
- No reasoning
- No decision logic
- No SOP interpretation

This cleanly simulates downstream operational systems.

---

## How Reasoning Flows 

1. **Orchestrator**
   - Determines what findings needed more
   - gets findings on the run from other agents and decides which agent to call next
   - Routes to the correct agent with passing agent task description
   - clearly manages chain of thought processing with exact investigation path resolution path with current findings
   - Central Hub for this Hub - Spoke Architecture

2. **Specialist Agent**
   - Computes or extracts a single finding
   - Updates shared state

3. **Orchestrator**
   - Re-evaluates remaining gaps
   - Continues routing or proceeds to adjudication

4. **Adjudicator**
   - Applies SOP rules
   - Finalizes decision

5. **AEM**
   - Executes the required action

Reasoning is represented through **state transitions**, not hidden chain-of-thought.

---
