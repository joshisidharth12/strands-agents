# Strands Agents Study Plan

**Goal:** Go from a local Strands agent to production on AWS AgentCore, deployed with Strands + AWS CDK.

**Your starting point:** You already have a working local agent (`agent.py`) using LiteLLM (Groq), a custom `@tool`, and basic invocation. This plan builds from there.

**Estimated timeline:** ~4–6 weeks at ~8–10 hrs/week (adjust freely).

**Primary docs:**
- [Strands Agents Docs](https://strandsagents.com/docs/)
- [Strands Learning Path](https://strandsagents.com/docs/learning/how-agents-really-work/)
- [Amazon Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-agentcore.html)
- [CDK `aws-bedrockagentcore` constructs](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore-readme.html)

---

## Learning path overview

```
Phase 0  Foundations & mental model
Phase 1  Local Strands mastery (all SDK aspects)
Phase 2  AgentCore platform (services + how they fit)
Phase 3  Deploy: Strands → AgentCore (CLI first, then CDK)
Phase 4  Capstone: production-shaped agent on CDK + AgentCore
```

---

## Phase 0 — Foundations (1–2 days)

**Outcome:** Clear mental model of *agent = model + harness*.

### Concepts
- [ ] Models are stateless; agents add loop, tools, memory, and control
- [ ] The agent loop: context → reason → tool? → result → repeat
- [ ] Three layers: prompt engineering, context engineering, harness engineering
- [ ] Strands is a **library** (runs in your process), not a hosted platform
- [ ] AgentCore is the **AWS platform** for running, securing, and operating agents at scale

### Do
- [ ] Read [Lesson 1: How agents really work](https://strandsagents.com/docs/learning/how-agents-really-work/)
- [ ] Re-run your existing `agent.py` and inspect `agent.messages` after a call
- [ ] Sketch (on paper) what happens when your weather tool is invoked

### Checkpoint
Explain in one paragraph: what Strands owns vs what the model owns vs what AgentCore will own later.

---

## Phase 1 — Local Strands mastery (1.5–2 weeks)

Cover every major SDK surface before touching AWS. Prefer small, focused scripts under something like `study/` or notebooks from the [samples repo](https://github.com/strands-agents/samples).

### 1.1 Agent core & invocation
- [ ] `Agent(...)` construction: model, tools, system prompt
- [ ] Sync invoke vs streaming (`stream` / async patterns)
- [ ] Structured output
- [ ] Conversation history and `agent.messages`
- [ ] System prompts and steering / behavioral boundaries

**Practice:** Extend your weather agent with a system prompt and structured output for “location + temp + condition”.

**Docs:** [Python Quickstart](https://strandsagents.com/docs/user-guide/quickstart/python/)

### 1.2 Model providers
- [ ] Default: Amazon Bedrock
- [ ] Providers you already use: LiteLLM
- [ ] Local: Ollama
- [ ] Others: OpenAI, Anthropic, Google, custom providers
- [ ] When to switch providers vs keep abstraction (LiteLLM)

**Practice:** Run the same agent with (1) Groq via LiteLLM, (2) Bedrock, (3) Ollama if available. Note API/key differences only.

**Docs:** [Model providers](https://strandsagents.com/docs/user-guide/sdk/model-providers/ollama/)

### 1.3 Tools
- [ ] `@tool` decorator: docstrings + type hints → schema
- [ ] Error handling inside tools
- [ ] Vended / community tools (`file_editor`, `shell`, `web_fetch`, etc.)
- [ ] Tool result size and context pressure
- [ ] Parallel / batched tool calls (conceptually)

**Practice:** Build 3–4 tools (e.g. weather, calculator, file note, fake DB lookup) and force multi-tool workflows.

### 1.4 MCP (Model Context Protocol)
- [ ] What MCP is and why it matters for tool ecosystems
- [ ] Transports: stdio, Streamable HTTP, SSE
- [ ] Attaching one MCP server to a Strands agent
- [ ] Multiple MCP servers in one agent
- [ ] Auth patterns for remote MCP (high level)

**Practice:** Connect at least one local MCP server (stdio) and call its tools from Strands.

**Docs:** [MCP tools](https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/)

### 1.5 Context & conversation management
- [ ] Null / sliding-window / summarizing managers
- [ ] `context_manager="auto"` behavior (offload, compress, proactive)
- [ ] What belongs in short-term conversation vs long-term memory

**Practice:** Run a long multi-turn chat that would overflow a naive window; observe summarization / truncation behavior.

### 1.6 Sessions & state
- [ ] Session managers: File, S3, repository-style
- [ ] Persisting agent state across process restarts
- [ ] Actor / session identity (local analogue of AgentCore sessions)

**Practice:** Restart a script mid-conversation and resume from a file-backed session.

### 1.7 Hooks & lifecycle
- [ ] Hook providers vs callbacks
- [ ] Key events: before/after invocation, model call, tool call
- [ ] Use cases: logging, validation, guardrails, cancel/retry, human-in-the-loop
- [ ] Multi-agent hook events (preview for next section)

**Practice:** Log every tool call; block a dangerous tool via `BeforeToolCallEvent`.

**Docs:** [Hooks](https://strandsagents.com/docs/user-guide/sdk/agents/hooks/) · [Hook events](https://strandsagents.com/docs/user-guide/sdk/agents/hooks-events/)

### 1.8 Multi-agent patterns
- [ ] Agents-as-tools
- [ ] Swarm
- [ ] Graph
- [ ] Workflow
- [ ] Agent-to-Agent (A2A) protocol (concept + when to use)

**Practice:** Build a 2–3 agent system (researcher → writer → reviewer) using Graph or Workflow.

### 1.9 Observability & evaluation (local)
- [ ] OpenTelemetry integration in Strands
- [ ] Tracing tool/model steps locally
- [ ] Basic eval mindset: task success, tool correctness, regression cases

**Practice:** Emit traces for one multi-tool run and read them.

### Phase 1 checkpoint
You can build a **local** multi-tool, multi-turn, optionally multi-agent Strands app with hooks, MCP, and session persistence — without AWS.

---

## Phase 2 — Amazon Bedrock AgentCore (1–1.5 weeks)

**Outcome:** Know every AgentCore service, what problem it solves, and how it maps to Strands primitives.

### Mental model

| You build in Strands (local) | AgentCore provides in AWS |
| --- | --- |
| Agent loop / orchestration code | **Runtime** (serverless microVM sessions) or managed **Harness** |
| Conversation / custom memory | **Memory** (short-term + long-term strategies) |
| MCP / custom tools | **Gateway** (API/Lambda → MCP tools) + Policy |
| Process identity / API keys | **Identity** (IdP, OAuth, IAM) |
| Local shell / code experiments | **Code Interpreter** sandbox |
| Local browser automation | **Browser** tool runtime |
| Local OTEL logs | **Observability** (CloudWatch + OTEL) |
| Manual eval scripts | **Evaluations** (+ **Optimization**) |
| Ad-hoc tool catalogs | **Registry** |
| Paid tool access | **Payments** (x402 / MPP) |

### 2.1 Platform overview
- [ ] Read [What is AgentCore?](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-agentcore.html)
- [ ] Distinguish: **Harness** (managed loop, config-first) vs **Runtime** (bring your Strands code)
- [ ] Framework-agnostic design (Strands, LangGraph, CrewAI, etc.)
- [ ] Consumption pricing mindset (no infra babysitting, pay for use)

### 2.2 Runtime (highest priority for Strands deploy)
- [ ] Session isolation via microVMs
- [ ] Cold starts, long-running / async agents
- [ ] Required HTTP contract for custom containers: `POST /invocations`, `GET /ping`
- [ ] Build types: **CodeZip** vs **container (ECR)**
- [ ] Runtime versioning & endpoints
- [ ] Network (public / VPC) and IAM execution role
- [ ] Auth on the runtime endpoint

**Docs:** [Runtime how it works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html) · [CLI get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html)

### 2.3 Memory
- [ ] Short-term (multi-turn) vs long-term (cross-session)
- [ ] Strategies (e.g. semantic, user preference) and sharing across agents
- [ ] How Strands session/conversation concepts map to AgentCore Memory
- [ ] Actor ID / session ID discipline (never trust client blindly in prod)

### 2.4 Gateway + Policy
- [ ] Turn OpenAPI / Smithy / Lambda into MCP tools
- [ ] Ingress vs egress auth
- [ ] Gateway targets, naming, interceptors
- [ ] **Policy** / Dogwood (Cedar-compatible) for deterministic tool allow/deny

### 2.5 Identity
- [ ] Cognito / Okta / Entra / Auth0 compatibility
- [ ] User-delegated OAuth for tools vs runtime IAM
- [ ] Why Identity matters for multi-tenant agents

### 2.6 Built-in tool runtimes
- [ ] **Code Interpreter**: languages, sandbox, VPC modes
- [ ] **Browser**: Playwright/BrowserUse style automation, recording

### 2.7 Ops & quality services
- [ ] **Observability:** traces, spans, CloudWatch views
- [ ] **Evaluations:** session/trace-based quality signals
- [ ] **Optimization:** prompt/tool-description experiments, A/B via Gateway
- [ ] **Registry:** catalog of agents/tools/MCP servers
- [ ] **Payments:** optional; skim unless you need paid tool access

### Phase 2 checkpoint
For a “customer support agent with CRM tools and memory,” draw which AgentCore services you would use and why. Know when you’d choose **Harness** vs **code-based Strands on Runtime**.

---

## Phase 3 — Deployment path (1.5–2 weeks)

Deploy the same Strands agent three ways, in order. Each step teaches a layer the next one automates.

### Track A — AgentCore CLI (fastest path to “it runs on AWS”)
**Why first:** Validates Runtime packaging, invoke, memory, and observability without writing IaC.

- [ ] Install CLI: `npm install -g @aws/agentcore`
- [ ] AWS account + Bedrock model access + credentials
- [ ] Scaffold: `agentcore create --name MyProject --template agent-python-strands`
- [ ] Understand generated layout (`main.py`, `agentcore.json`, CDK under the hood)
- [ ] Local: `agentcore dev` (and Inspector if useful)
- [ ] `agentcore build` → `agentcore deploy`
- [ ] `agentcore invoke` with session IDs
- [ ] Add Memory: `agentcore add memory ...`
- [ ] Compare **CodeZip** template vs **container** template (`agent-python-strands-container`)

**Docs:**
- [Get started with AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html)
- [Strands → AgentCore deploy](https://strandsagents.com/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)
- [Lesson 14: Deploying agents to the cloud](https://strandsagents.com/docs/learning/deploying-agents-to-the-cloud/)

**Practice:** Port your local weather (or richer) agent into the scaffolded `main.py`, deploy, invoke remotely.

### Track B — Manual Runtime packaging (understand the contract)
**Why:** So CDK isn’t magic.

- [ ] Entrypoint + Bedrock AgentCore app wrapper (`@app.entrypoint` pattern)
- [ ] Dependencies for Runtime (e.g. `bedrock-agentcore`, `strands-agents`)
- [ ] ARM64 / platform constraints for CodeZip or images
- [ ] ECR push path for containers
- [ ] IAM: `bedrock:InvokeModel` (+ inference profile / Marketplace as needed)
- [ ] Invoke via `boto3` `bedrock-agentcore` client

**Docs:** [Python deploy to AgentCore Runtime](https://strandsagents.com/docs/user-guide/sdk/deploy/deploy_to_bedrock_agentcore/python/)

### Track C — Strands + AWS CDK + AgentCore (your target stack)
**Why:** Repeatable, reviewable infra for real projects.

Learn and practice **both** CDK approaches (pick one as primary later):

#### C1 — Direct CDK L2 constructs (`aws-bedrockagentcore` / alpha packages)
- [ ] Read CDK AgentCore README (Runtime, Memory, Gateway, Browser, Code Interpreter, Policy, Evaluations)
- [ ] Create `Runtime` with `AgentRuntimeArtifact.fromCodeAsset` **or** `fromEcrRepository`
- [ ] Wire execution role permissions (Bedrock invoke, logs, memory, gateway as needed)
- [ ] Outputs: Runtime ARN / endpoint
- [ ] Versioning: what changes create a new runtime version
- [ ] Optional: Memory + Gateway constructs in the same stack
- [ ] Synth / deploy / invoke smoke test

**References:**
- [CDK AgentCore construct library](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore-readme.html)
- Practical walkthrough: [AgentCore CDK quickstart](https://sph.sh/en/posts/agentcore-cdk-quickstart/)

**Minimal mental checklist for a CDK stack:**
1. Package agent artifact (zip or ECR image)
2. `Runtime` construct + name constraints (e.g. camelCase where required)
3. IAM for models and AWS APIs the agent needs
4. Optional Memory / Gateway / Identity / Observability wiring
5. `cdk deploy` → invoke → CloudWatch traces

#### C2 — Nx Plugin for AWS (scaffolded CDK)
- [ ] Create workspace with `@aws/nx-plugin` (choose **CDK**)
- [ ] Generate Python project + Strands agent (`py#agent`)
- [ ] Generate infra project; instantiate agent construct in application stack
- [ ] `pnpm build` → `pnpm nx deploy infra`
- [ ] Compare generated Dockerfile / constructs with your hand-written CDK from C1

**Docs:** [Deploy with Nx Plugin for AWS](https://strandsagents.com/docs/user-guide/deploy/deploy_with_nx_plugin_for_aws/)

### Phase 3 checkpoint
Same agent logic runs:
1. locally with Strands,
2. on AgentCore via CLI,
3. on AgentCore via **your** CDK stack (with clear IAM and artifact story).

---

## Phase 4 — Capstone (3–5 days)

Build one end-to-end project that forces the full path.

### Suggested capstone: “Ops assistant”
**Local (Strands)**
- Custom tools + at least one MCP server
- Hooks for audit logging / tool allowlist
- File or local session persistence
- Optional: 2-agent graph (triage → specialist)

**AgentCore**
- Deploy on **Runtime** (CodeZip or container)
- Attach **Memory** (semantic and/or user preference)
- Expose one backend via **Gateway** (Lambda or OpenAPI)
- Turn on **Observability**; run one **Evaluation** pass if time allows
- Identity: at least IAM invoke path; OAuth/Cognito if you need user context

**CDK**
- Single app with stacks/constructs for Runtime (+ Memory/Gateway as needed)
- Parameterize model ID, region, runtime name
- Document deploy / invoke / teardown

### Capstone definition of done
- [ ] `cdk deploy` (or Nx deploy) from a clean clone works with documented prerequisites
- [ ] Remote invoke with stable `session_id` / `actor_id` behavior
- [ ] You can point to traces in Observability for a failed tool call
- [ ] You can explain every AWS resource in the stack and why it exists

---

## Suggested weekly schedule

| Week | Focus |
| --- | --- |
| 1 | Phase 0 + Phase 1.1–1.5 (agent, models, tools, MCP, context) |
| 2 | Phase 1.6–1.9 (sessions, hooks, multi-agent, local OTEL) |
| 3 | Phase 2 full AgentCore tour + Runtime deep dive |
| 4 | Phase 3 Tracks A + B (CLI + manual packaging) |
| 5 | Phase 3 Track C (CDK L2 and/or Nx) |
| 6 | Phase 4 capstone + cleanup / notes |

Compress to 4 weeks by merging weeks 5–6 if you already know CDK.

---

## Aspect coverage checklist (use as a final audit)

### Strands (local)
- [ ] Agent loop & harness mental model
- [ ] Models & providers (Bedrock, LiteLLM, Ollama, others)
- [ ] Custom tools & vended tools
- [ ] MCP integration
- [ ] Streaming & structured output
- [ ] Conversation / context managers
- [ ] Sessions & state
- [ ] Hooks & lifecycle events
- [ ] Multi-agent (swarm / graph / workflow / A2A / agents-as-tools)
- [ ] Observability (OTEL) & basic evals
- [ ] Steering / system prompt design

### AgentCore
- [ ] Harness vs Runtime decision
- [ ] Runtime (sessions, artifacts, endpoints, IAM, networking)
- [ ] Memory
- [ ] Gateway + Policy
- [ ] Identity
- [ ] Code Interpreter
- [ ] Browser
- [ ] Observability
- [ ] Evaluations & Optimization
- [ ] Registry (awareness)
- [ ] Payments (awareness)

### Deploy (Strands + CDK + AgentCore)
- [ ] AgentCore CLI workflow
- [ ] CodeZip vs container packaging
- [ ] Runtime HTTP contract / entrypoint
- [ ] CDK Runtime (+ Memory/Gateway) constructs
- [ ] IAM for Bedrock + agent permissions
- [ ] Invoke, version, observe, tear down
- [ ] Optional: Nx Plugin CDK path

---

## How to study day-to-day

1. **Read → tiny experiment → write 5 bullet notes** (what broke, what clicked).
2. Prefer modifying **this repo** over collecting unread bookmarks.
3. After each phase checkpoint, teach the concept out loud or in a short README section.
4. Keep AWS cost hygiene: destroy stacks when idle; start with CodeZip / small models.

---

## Quick reference — commands you’ll use a lot

```bash
# Local (this project)
uv sync
uv run python agent.py

# AgentCore CLI
npm install -g @aws/agentcore
agentcore create --name MyProject --template agent-python-strands
agentcore dev
agentcore build
agentcore deploy
agentcore invoke --runtime agent --payload '{"prompt":"Hello"}'
agentcore status

# CDK (once you have a stack)
cdk synth
cdk deploy
cdk destroy
```

---

## Resources index

### Strands
- Learning lessons: https://strandsagents.com/docs/learning/how-agents-really-work/
- Deploy to AgentCore: https://strandsagents.com/docs/user-guide/deploy/deploy_to_bedrock_agentcore/
- Deploy with Nx + CDK: https://strandsagents.com/docs/user-guide/deploy/deploy_with_nx_plugin_for_aws/
- Samples: https://github.com/strands-agents/samples

### AgentCore
- Overview: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-agentcore.html
- CLI quickstart: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html
- Runtime CLI path: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html

### CDK
- AgentCore constructs: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore-readme.html
- Example walkthrough: https://sph.sh/en/posts/agentcore-cdk-quickstart/
