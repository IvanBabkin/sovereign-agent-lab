"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venue found — the largest available venue (The Guilford Arms, 200 capacity) is under 300, and no venue with both 300+ capacity and vegan options exists in the dataset."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changing The Albanach's status to 'full' in mcp_venue_server.py caused it to
disappear from all search results automatically. In Query 1, search_venues
returned 1 match instead of 2; the agent still found the correct answer (The
Haymarket Vaults) without any guidance. In Query 2, The Albanach was also
absent when the agent probed lower capacity thresholds.

No changes were needed to exercise4_mcp_client.py, the tool bridge code, or
the tool schemas. Only mcp_venue_server.py was edited. The agent picked up the
updated data at runtime because each MCP call spawns a fresh server process
reading the current file — there is no caching or redeployment step.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 8   # task_d hardcodes 4 tool names: import block (220-223) + tool list in create_react_agent (232-235)
LINES_OF_TOOL_CODE_EX4 = 0   # grep confirms: exercise4_mcp_client.py never mentions search_venues or get_venue_details

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP separates the tool layer at the protocol level, not just the file level.
The server runs as an independent process over stdio, so any client — LangGraph,
Rasa, a CLI script, a different language entirely — can connect without sharing
Python imports or dependencies. Tools are discovered dynamically at runtime:
add a @mcp.tool() to the server and every client picks it up automatically
with no code changes. Data changes (like flipping a venue status) propagate
instantly because each call spawns a fresh server session reading current state,
with no caching or redeployment step needed.

Caveat: MCP is not free. Exercise 4 contains ~37 lines of generic bridge code
(_build_args_schema, _make_mcp_caller, discover_tools) that Exercise 2 does not
need. The win is that this bridge is written once and stays tool-agnostic —
zero lines reference specific tools — so adding or removing tools on the server
never requires touching the agent file, whereas Exercise 2's 8 hardcoded lines
in task_d must be edited for every change to the tool set.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The MCP venue server acts as the shared tool layer so that both the LangGraph
  agent and the Rasa action server can access live venue data without duplicating
  business logic or maintaining separate tool codebases.
- The LangGraph research agent (powered by DeepSeek R1 for planning and Llama
  70B for execution (or potentially other models if fixes needed))
  handles open-ended research tasks because it can autonomously
  decide the sequence of tool calls needed, as demonstrated when it probed six
  progressively lower capacity thresholds to map the dataset in Query 2.
- The Rasa CALM dialogue manager handles the booking confirmation conversation
  because it enforces a predictable, auditable flow (venue → guests → catering →
  confirm) that cannot be improvised away by the model.
- The CLAUDE.md memory store persists user preferences, past venue choices, and
  catering budgets across sessions so the agent does not ask the same questions
  twice in future bookings.
- The observability layer tracks token cost, latency, and tool call success rates
  per session so that regressions (such as the infinite loop caused by a missing
  recursion_limit) are caught automatically rather than discovered by inspection.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph ReAct handles the research; Rasa CALM handles the booking call.

In Query 1, the LangGraph agent autonomously decided to call search_venues,
evaluate two candidates, pick the exact-fit venue, then call get_venue_details —
the step sequence was never specified. In Query 2, it improvised six separate
search_venues calls with progressively lower capacity thresholds to map the
dataset. No Rasa flow could express this open-ended exploration without writing
an explicit rule for every possible capacity probe.

Swapping feels wrong in both directions. Giving Rasa the research task would
require pre-defining every branch of venue exploration in flows.yml — impossible
for genuinely open queries. Giving LangGraph the booking call risks the model
skipping required confirmation steps or inventing fields, because its loop has
no structural guarantee that venue, guest count, and catering are all confirmed
before the booking fires. The two agents are optimised for opposite things:
one for freedom, one for discipline.
"""
