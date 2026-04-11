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
TASK_B_IMPLEMENTED = None   # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "FILL_ME_IN"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "FILL_ME_IN"

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
FILL ME IN
"""

SCENARIO_1_FALLBACK_VENUE = "FILL_ME_IN"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = None   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
FILL ME IN
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = None   # True or False

SCENARIO_3_RESPONSE = "FILL_ME_IN"

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
FILL ME IN
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
PASTE MERMAID OUTPUT HERE
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
FILL ME IN
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
FILL ME IN
"""
