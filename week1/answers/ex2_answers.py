"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Note to the grader: structural changes made to the scaffold ────────────
# Please read this before grading. The full text is in STRUCTURAL_CHANGES_NOTE below
# so it shows up alongside the answers it explains.

STRUCTURAL_CHANGES_NOTE = """
Three changes were needed to make Exercise 2 actually run end-to-end on
this machine. Every one of them is preserved in the git history of this
branch (commits bef83d4 and ec67dd6).

1. Model swap in sovereign_agent/agents/research_agent.py
   meta-llama/Llama-3.3-70B-Instruct  ->  MiniMaxAI/MiniMax-M2.5
   Llama-3.3-70B on Nebius did not populate `message.tool_calls` — it
   emitted tool calls as plain text content instead. The ReAct loop
   therefore never executed any tool, and Task A's run produced
   `tool_calls_made: []`. MiniMax-M2.5 uses the standard OpenAI
   function-calling protocol, which is what the rest of the LangGraph
   pipeline expects. The new model is what produced ex2_results.json
   and the Task A answers below.

2. Tool-call parser in run_research_agent (same file)
   I added a primary branch that reads `m.tool_calls` (the LangChain /
   OpenAI-compatible field) before falling back to the original
   Anthropic-style `list[block]` parser. The original code only handled
   the Anthropic shape, which is why no tool calls were ever recorded
   even when the model was emitting them. The fallback is preserved so
   the parser still works if the scaffold is later pointed at an
   Anthropic-shaped model.

3. Wrong kwarg in week1/grade.py (Ex2 stub check)
   Line 168 of grade.py called the flyer tool as
       raw_fn(pub_name="Test", guest_count=10, event_theme="test")
   but the actual signature in venue_tools.py is
       generate_event_flyer(venue_name, guest_count, event_theme)
   So the grader's "is generate_event_flyer still a stub?" check failed
   on every correct implementation with a TypeError. I changed `pub_name`
   to `venue_name` (commit ec67dd6). No grading logic was changed —
   only the kwarg name to match the real function signature.

Task B note: my generate_event_flyer implementation calls the Nebius
image API (black-forest-labs/flux-schnell) via the OpenAI client. The
returned URL is in TASK_B_IMAGE_URL_OR_ERROR below.
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
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-82cfabb6-1097-4fa2-9168-3d795a057aca_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The Bow Bar only has a capacity of 80, which is insufficient for 160 guests. Let me check the other available venues.
(excluding thinking tags)
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
(excluding thinking tags)
Unfortunately, none of our known venues can accommodate 300 people. Here's the breakdown:

| Venue | Capacity | Vegan Options | Meets Requirements |
|-------|----------|---------------|-------------------|
| The Albanach | 180 | ✅ Yes | ❌ Too small |
| The Haymarket Vaults | 160 | ✅ Yes | ❌ Too small |
| The Guilford Arms | 200 | ❌ No | ❌ Too small & no vegan |
| The Bow Bar | 80 | ✅ Yes | ❌ Too small & currently full |

The largest venue we have is **The Guilford Arms** with a capacity of 200, but it doesn't offer vegan options.

Would you like to:
1. Reduce the guest count to 200 or less to fit within our existing venues?
2. Consider a different venue outside our known list?

Let me know how you'd like to proceed!
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = """
I don't have access to train schedule information or any tools that would allow me to look up train times.
My available tools are focused on Edinburgh venues, weather, catering costs, and event flyer generation.

To find the last train from Edinburgh Waverley to London tonight, I'd recommend:
1. National Rail (nationalrail.co.uk) or ScotRail (scotrail.co.uk) websites
2. Trainline app or website (trainline.com)
3. Checking real-time departure boards at Edinburgh Waverley station

Is there anything else I can help you with? I can assist with finding a pub or venue in Edinburgh if that's of interest.
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
The most unexpected behaviour was in Scenario 1: after The Bow Bar failed, the agent checked only The Albanach —
found it met all requirements — and stopped immediately without checking the remaining venues. The task prompt
said "check any other available venue" (singular), and the model read that literally: find one, stop. This
contrasts with Task A where the model proactively checked both venues in parallel even though "if one works" also
implied a single venue was sufficient. The agent applied a different stopping strategy based on subtle wording
differences ("any other" vs. "check both"), which is emergent reasoning about scope that was never explicitly
instructed.
"""
