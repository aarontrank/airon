# Multi-Agent System Blueprint

## Purpose

This document is a reference for AI agents and developers configuring or executing a multi-agent system. It defines architecture, contracts, and operational rules that govern how agents are built, coordinated, and improved over time.

---

## Architecture Overview

The system has three layers:

| Layer | Purpose |
|---|---|
| **Agent Definition** | Reusable agent templates (job, persona, capabilities) |
| **Project Configuration** | Contextual specialization for a specific use case |
| **System Layer** | Orchestration, memory, learning, governance |

**Core formula:**

```
Agent = Job (What) + Persona (How) + Capabilities (What it can access/do)
```

---

## Separation of Concerns

| Concern | Lives In |
|---|---|
| What the agent does | Agent Definition |
| How it behaves | Agent Definition |
| Project-specific context | Project Config |
| Tool access | Project Config |
| Task coordination | Orchestrator |
| Permissions & approvals | Governance Layer |
| Learning & improvement | System Layer |
| Memory implementation | System Layer |

---

## Layer 1: Agent Definition

Agent definitions are **reusable templates**. They must not contain project-specific context.

### Required Fields

#### `job`
The agent's primary responsibility. Examples: `ContentCreator`, `EngagementManager`, `FinancialAnalyst`, `Orchestrator`.

#### `persona`
How the agent reasons and makes decisions.

| Role Type | Behavior |
|---|---|
| Junior executor | Follows instructions strictly |
| Senior strategist | Makes higher-level decisions |
| Domain expert | Applies specialized knowledge |

#### `inputs`
Standardized input schema all agents must accept:

```json
{
  "task": "string",
  "context": "object",
  "constraints": "object"
}
```

#### `outputs`
Standardized output schema all agents must return:

```json
{
  "status": "success | failure | needs_review",
  "result": "object",
  "errors": "array",
  "next_actions": "array"
}
```

> **Critical:** Consistent output structure is required for orchestration to function. Deviating from this schema breaks agent compatibility.

#### `error_handling`
All agents must signal one of:
- `failure` — unrecoverable, do not retry
- `retryable` — transient error, safe to retry
- `needs_human_review` — ambiguous, escalate

#### `autonomy`
Defines the agent's default authority level:
- `full` — acts without approval
- `conditional` — acts unless confidence is below threshold
- `approval_required` — always waits for human sign-off

#### `tools`
Declares tool capability — not which tools (that lives in Project Config):
- `can_use_tools: true/false`
- `can_create_tools: true/false`
- `tool_usage_policy: when to prefer tools vs reasoning`

#### `memory`
Declares memory interaction capability — not implementation:
- `read: true/false`
- `write: true/false`
- `memory_types: [episodic, semantic, procedural]`

### Example Agent Definition

```yaml
agent_name: ContentCreator

job: Generate short and long-form content

persona:
  role: Senior Content Strategist
  traits:
    - clear
    - persuasive
    - audience-aware

inputs:
  - task
  - messaging_pillars
  - audience

outputs:
  format: structured_json

autonomy:
  level: conditional
  requires_review_for:
    - long_form_content

memory:
  read: true
  write: true

tools:
  can_use_tools: true
  can_create_tools: false
```

---

## Layer 2: Project Configuration

Project configs **specialize** an agent definition for a specific use case. They do not redefine the agent's job or persona.

### Required Fields

#### `goal`
The mission this project serves.

```yaml
goal: Match volunteers to community projects and coordinate execution for WorkForGood
```

#### `audience`
Who the agent is operating for or communicating with.

```yaml
audience:
  primary: volunteers and community partners
  tone: warm, clear, action-oriented
```

#### `messaging_pillars`
Core themes the agent should reinforce.

```yaml
pillars:
  - community impact
  - volunteer empowerment
  - reliable coordination
```

#### `tools`
Which specific tools the agent may use in this project.

```yaml
tools:
  - volunteer_registry_api
  - project_board_api
  - notification_service
  - calendar_api
```

#### `autonomy_overrides`
Per-agent overrides to the default autonomy level.

```yaml
autonomy_overrides:
  scheduling_agent:
    requires_approval: false
  outreach_agent:
    requires_approval: true
```

#### `pipeline` *(optional)*
Defines the expected task execution sequence.

```yaml
pipeline:
  - assess_project_needs
  - match_volunteers
  - confirm_assignments
  - send_notifications
  - monitor_completion
```

---

## Layer 3: System Layer

### 3.1 Orchestration

The orchestrator is responsible for:
- Assigning tasks to agents
- Managing execution flow
- Handling retries on failure
- Routing agent outputs to next steps

#### Orchestrator Types

| Type | Behavior | Use When |
|---|---|---|
| Script-based | Fixed pipeline, deterministic | Simple, predictable flows |
| Agent-based | Dynamic, decision-making | Ambiguous or adaptive flows |

#### Hierarchical Orchestration

Structure orchestrators like an organization chart:

```
[CEO Orchestrator]
        |
[Volunteer Orchestrator]   [Operations Orchestrator]
        |                          |
[Matching Agent]          [Scheduling Agent]
[Outreach Agent]          [Follow-up Agent]
```

Benefits: scalability, domain separation, specialization at each level.

---

### 3.2 Triggers (Execution Model)

| Type | Mechanism | Use For |
|---|---|---|
| Scheduled | Cron | Daily project status checks, weekly volunteer digests |
| Event-driven | Webhooks, watchers | New project submitted, volunteer signs up, assignment declined |

**Recommended:** Hybrid model — cron for consistency, events for responsiveness.

---

### 3.3 Memory Layer

#### Two Implementation Levels

| Level | Storage | Best For |
|---|---|---|
| 1 | JSON / Markdown context files | Early stage, simple systems |
| 2 | Knowledge base / RAG | Long-term learning, large history |

#### Design Principle

Agents must depend on a **memory interface**, not a specific implementation:

```
[Agent]
   |
[Memory Interface]
   /          \
[Context File]  [RAG System]
```

This allows the underlying storage to be swapped without changing agent code.

---

### 3.4 Learning System (Meta Layer)

The learning layer evaluates outcomes and improves the system over time.

#### Implementation Options

| Option | Mechanism | Effort |
|---|---|---|
| A | Logging + human review | Low, manual |
| B | Learning agent (recommended) | Higher, automated |

A **learning agent** operates as a meta-agent that:
- Reviews task outputs and logs
- Detects failure patterns
- Proposes config or prompt improvements

#### What It Can Update
- Project configs
- Prompt templates
- Tool usage rules

> **Warning:** The learning agent must NOT directly rewrite core agent definitions without explicit safeguards and human approval.

#### Feedback Loop

```
[Agents Execute]
       |
[Logs + Outcomes]
       |
[Learning Agent]
       |
[Updated Configs / Insights]
```

---

### 3.5 Governance Layer

Governance defines rules about who can change what, what requires approval, and how actions are audited.

#### Permissions

| Action | Requires |
|---|---|
| Modify agent definitions | Elevated permission |
| Change project configs | Owner approval |
| Deploy agents to production | Reviewed + approved |

#### Approval Gates
Actions that always require human approval:
- Publishing content publicly
- Financial decisions
- Public-facing responses
- Agent definition changes

#### Audit Logs
Every agent action must log:
- What happened
- Why it happened
- Which agent acted
- Timestamp

#### Governance Overlay

```
       [Governance Layer]
              |
[Orchestrator → Agents → Outputs]
              ↑
         [Audit Logs]
```

---

## Standardization Requirements

Without standardization, orchestrators break, agents become incompatible, and debugging becomes impossible.

### Required Standards

| Contract | Requirement |
|---|---|
| Inputs | Consistent schema across all agents |
| Outputs | Structured JSON with predictable fields |
| Errors | Shared error vocabulary (`failure`, `retryable`, `needs_human_review`) |
| Timing | Defined response behavior (timeout, retry count) |

---

## Tooling Model

### Three Levels of Tool Usage

| Level | Description |
|---|---|
| 0 | No tools — reasoning only |
| 1 | Tool usage — calls external APIs or functions |
| 2 | Tool creation — generates reusable tools dynamically |

### Where Tool Access Is Defined

| Aspect | Location |
|---|---|
| Can the agent use tools? | Agent Definition |
| Which tools are available? | Project Config |

---

## Evolution Strategy

Build the system in phases to avoid premature complexity.

### Phase 1: Simple System
- Cron-triggered execution
- Single-purpose agents
- Context files for memory

### Phase 2: Structured System
- Orchestrator introduced
- Standardized I/O enforced
- Multiple coordinated agents

### Phase 3: Advanced System
- Event-driven triggers added
- Knowledge base or RAG for memory
- Learning agent introduced

### Phase 4: Organizational System
- Hierarchical orchestrators
- Governance layer enforced
- Fully autonomous workflows

---

## End-to-End Example: WorkForGood

WorkForGood is a non-profit that coordinates volunteers to complete community projects — things like neighborhood cleanups, food bank staffing, tutoring programs, and park restoration. The system automates matching, scheduling, and follow-up so staff can focus on relationships and impact.

A concrete walkthrough of a full system execution.

```
1. Trigger
   └─ New community project submitted via intake form
      OR weekly cron to re-evaluate unfilled slots

2. CEO Orchestrator
   └─ Assesses project priority and resource availability
   └─ Routes to Volunteer Orchestrator + Operations Orchestrator

3. Volunteer Orchestrator
   └─ Breaks goal into subtasks:
      - volunteer matching
      - outreach and confirmation
      - waitlist management

4. Matching Agent
   └─ Queries volunteer registry for availability, skills, location
   └─ Returns ranked candidate list

5. Outreach Agent (conditional approval)
   └─ Drafts and sends personalized invitations
   └─ Flags first-contact messages for staff review before sending

6. Confirmation Agent
   └─ Tracks RSVPs, handles declines, pulls from waitlist

7. Operations Orchestrator
   └─ Breaks execution into subtasks:
      - scheduling and calendar
      - day-of notifications
      - completion tracking

8. Scheduling Agent
   └─ Creates calendar events, assigns roles, resolves conflicts

9. Notification Agent
   └─ Sends reminders 48h and 2h before project start

10. Memory Layer
    └─ Logs volunteer participation, project outcomes, no-show rates

11. Learning Agent
    └─ Evaluates match quality and volunteer retention trends
    └─ Surfaces suggestions (e.g., adjust matching criteria, update outreach tone)
```

---

## Mental Model

| System Component | Organizational Analogue |
|---|---|
| Agents | Employees |
| Orchestrators | Managers |
| CEO Orchestrator | Executive strategy |
| Project Config | Mission & operating context |
| Memory Layer | Institutional knowledge |
| Learning System | Continuous improvement process |
| Governance Layer | Leadership & accountability |
