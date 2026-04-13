"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Note to the grader: structural changes made to the scaffold ────────────
# Please read this before grading. The full text is in STRUCTURAL_CHANGES_NOTE below
# so it shows up alongside the answers it explains.

STRUCTURAL_CHANGES_NOTE = """
One scaffold fix was needed for Exercise 3 to grade correctly on Windows
(commit 56794e1). It does not affect any answer or any business logic.

1. UnicodeDecodeError in week1/grade.py (check_ex3)
   The scaffold called
       source = actions_path.read_text()
   on exercise3_rasa/actions/actions.py to verify the cutoff guard. On
   Windows, Path.read_text() defaults to the system codec (cp1252), which
   cannot decode the GBP sign in the file (e.g. "MAX_DEPOSIT_GBP = 300"
   and the £ symbols in the validation messages). The check therefore
   crashed with UnicodeDecodeError before it could even look at the guard,
   masking a passing implementation as a hard failure. I added an explicit
   encoding so the read succeeds on every platform:
       source = actions_path.read_text(encoding="utf-8")
   No grading logic was changed — only the file open mode. Mac/Linux
   default to utf-8 and were never affected.
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  no thank you
I'm sorry, I'm not trained to help with that.
Okay, I'll be around in case you need further help.
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £1,000 deposit
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £1000 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  i see, sure call me back in 15
I'm sorry, I'm not trained to help with that.
Okay, I'll be around in case you need further help.
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £1000 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM suspended the confirm_booking flow, triggered handle_out_of_scope, and offered to resume.
When the user said 'yes', CALM resumed and the flow continued as expected — however, it did not come back
to verify the number of vegan guests. The vegan_count slot was silently skipped, jumping straight to the
deposit question. This suggests the LLM treated 'yes' as filling the vegan_count slot rather than
as a resumption confirmation, leaving that data uncollected.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the deflection structurally: it triggered a dedicated handle_out_of_scope flow
and explicitly offered to resume the paused confirm_booking flow — behaviour that is hardwired in flows.yml
and identical every time, regardless of what the user said.
LangGraph responded to off-topic input via the LLM at runtime, which meant the reply could be more
contextually natural but was less predictable. CALM's approach is auditable and consistent, but the
conversation above shows a real cost: the LLM misinterpreted 'yes' as a vegan_count value, skipped a slot,
and then misfired the out-of-scope handler a second time on a perfectly valid deposit message.
LangGraph could improvise past such glitches; CALM's deterministic flows can compound them.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Temporarily changed the cutoff condition to 'if True:' to force the guard to always fire.
Ran a full booking conversation (160 guests, 50 vegan, £200 deposit) and confirmed the agent
escalated with the message: 'it is past 16:45 — insufficient time to process the confirmation
before the 5 PM deadline.' Then reverted the condition back to the real time check.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM eliminates the FormValidationAction and nlu.yml entirely. The LLM now handles what Python
previously did: parsing natural language slot values like 'about 160 people' into 160.0, and
deciding which flow to trigger from a description rather than matched intents.

Python still enforces the business rules in ActionValidateBooking class — deposit limits, capacity
ceilings, vegan ratios — because these constraints must be deterministic. An LLM could be
reasoned around; Python cannot.

The old approach was arguably more trustworthy for slot extraction: regex either matched or it
didn't. With from_llm, the extraction is probabilistic — as conversation 3 showed, 'yes' was
silently treated as a vegan count, skipping the slot entirely. More flexibility, less predictability.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The setup cost bought auditability and control. Every path the CALM agent can take is explicitly
written in flows.yml — a non-engineer can read it and know exactly what the agent will do.
The agent cannot improvise a response it wasn't trained on, and it cannot call a tool not defined
in flows.yml. For this confirmation use case, that is a feature: Rod needs to know the agent will
never go off-script on a financially binding decision.

LangGraph could improvise, tool-call dynamically, and handle novel situations — but you cannot
read a mermaid graph and predict every possible response. For a research agent that is an asset;
for a venue booking agent handling deposits, it is a liability. The CALM setup cost buys a
compliance-ready, auditable agent at the price of zero flexibility outside the defined flows.
"""
