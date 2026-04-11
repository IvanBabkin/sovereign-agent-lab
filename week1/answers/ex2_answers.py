"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "get_edinburgh_weather",
    "calculate_catering_cost",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = """
1. Model batched the first three tool calls in parallel (both venue checks + weather) before reasoning on results.
(three tool_call entries appear back-to-back before the first AI reasoning message and the model mentioned in the <think> block:
"Let me start by checking both pubs and the weather in parallel since these are independent calls.")

2.The model chose The Albanach over The Haymarket Vaults despite both passing — it reasoned that 180 capacity > 160
gives a safety margin. This is emergent prioritization not instructed in the prompt. The task just said "if oneworks."

3. The model continued gracefully after the flyer stub error as it got "success: false" with a STUB error from
generate_event_flyer, but rather than stopping or retrying, it reported the failure and still delivered a complete
final answer for everything else.

4. Catering was calculated after venue confirmation, not before — the model correctly followed the tool's own
docstring constraint ("Use AFTER confirming a venue. Do NOT call before a venue is confirmed"). It read the tool
description and respected the ordering rule without being told to in the task prompt.
"""

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-5fe04f68-526e-46f3-8a8e-99c84ae90c09_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The Bow Bar only has capacity for 80 guests (needed 160) and is full. Let me check the other available venues.
(if thinking tags are excluded)
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach or The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
(exluding thinking tags)
Unfortunately, none of our known venues can accommodate 300 people with vegan options. Here's the breakdown:

| Venue | Capacity | Vegan Options | Meets Requirements |
|-------|----------|---------------|-------------------|
| The Albanach | 180 | ✅ Yes | ❌ Too small |
| The Haymarket Vaults | 160 | ✅ Yes | ❌ Too small |
| The Guilford Arms | 200 | ❌ No | ❌ Too small, no vegan |
| The Bow Bar | 80 | ✅ Yes | ❌ Too small, currently full |

The largest venue we have is The Guilford Arms with a capacity of 200, which is still well below your requirement of 300 guests.

**Options:**
1. Consider a different type of venue outside our known list
2. Reduce the guest count to 200 or less (which would work at The Guilford Arms, though they don't have vegan options)
3. Split the event across multiple venues

Would you like me to help with any of these alternatives?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = """
I don't have access to train schedules or real-time transportation information. 
The tools available to me are focused on Edinburgh venues, weather, catering costs, and event promotion.
"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this behaviour is acceptable and desirable. 
The agent correctly recognised it lacked the relevant tool, acknowledged its scope boundary honestly, 
directed the user to appropriate external resources (National Rail, Trainline), and invited them to return with an in-scope question
rather than hallucinating a train time or trying to force an irrelevant tool call.
This is exactly what a trustworthy assistant should do when asked something outside its domain.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
LangGraph (research agent): The graph has just three nodes — start, agent, tools, end — forming a single loop.
All routing is implicit: the model decides at every step whether to call a tool or terminate. The graph is a container, 
and the complexity lives entirely inside the model's reasoning.

Rasa CALM (flows.yml): Every possible task is an explicitly named flow (confirm_booking, handle_out_of_scope),
with ordered steps written in YAML — collect this slot, run this action. The LLM only decides WHICH flow to
trigger; after that, Rasa executes the steps deterministically. Every path is readable and auditable without
running the model.

Trade-off: LangGraph is flexible and can handle novel paths the designer didn't anticipate, but you cannot
predict or audit every execution path. Rasa CALM is predictable and transparent — every possible behaviour is
documented — but it cannot handle tasks outside the pre-written flows.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
FILL ME IN
"""
