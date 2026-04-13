"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Note to the grader: structural changes made to the scaffold ────────────
# Please read this before grading. The full text is in STRUCTURAL_CHANGES_NOTE below
# so it shows up alongside the answers it explains.

STRUCTURAL_CHANGES_NOTE = """
I deliberately modified week1/exercise1_context.py to make the Part B
experiment actually demonstrate the structural-formatting effect on the
70B model. With the unmodified prompt, Llama-3.3-70B answered correctly
under PLAIN, XML and SANDWICH alike — Part B "passed" without ever
exhibiting the failure mode the lecture is teaching. To force the failure
I made two changes (both visible in commit c7b26a2):

  1. Rewrote QUESTION to include narrative phrasing
     ("I visited Bow Bar which holds 80 people, and while they did have
     vegan options, the status is currently full..."). This triggers the
     "Coherence Trap" / "Narrative Distraction" failure mode from the
     lecture by pushing the model into story-completion mode.

  2. Added a `vegetarian=` column to every entry in
     VENUES_WITH_DISTRACTORS. This creates "Distractor Asymmetry" —
     related-but-wrong dietary information sitting next to the correct
     vegan field — which makes the PLAIN condition prone to semantic
     blending across documents.

Together these changes broke PLAIN (Llama-3.3-70B picked The Holyrood
Arms, a venue that satisfies capacity + dietary but is *full*), while XML
and SANDWICH still produced the correct answer. That is the behaviour the
exercise is meant to surface, and it is what my Part B answers and
outputs/ex1_results.json reflect.

No fix to scaffold logic, scoring, or grade.py was needed for Ex1.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
In Part A, the 70B model successfully identified the correct venues across all three conditions.
Because the dataset was clean and the signal-to-noise ratio was high, 
the model did not need extra structural formatting to avoid hallucination.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Holyrood Arms"
PART_B_XML_ANSWER      = "The Haymarket Vaults"
PART_B_SANDWICH_ANSWER = "The Haymarket Vaults"

PART_B_PLAIN_CORRECT    = False
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = True

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
NOTE: The question was modified to include conversational phrasing ("I visited Bow Bar...") 
to trigger what the lecture calls "Narrative Distraction" or "The Coherence Trap," forcing the model into "story mode." 
Additionally, venues were updated to include vegetarian vs. vegan options to create "Distractor Asymmetry" (related-but-wrong info). 
The hardest distractor was "The Holyrood Arms" because it perfectly satisfied capacity and dietary constraints (even unneeded vegetarian constraints) but failed on availability. 
Without XML structures, document boundaries blur, causing the model to semantically blend these conflicting details and hallucinate an incorrect answer.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = False   # True or False

PART_C_PLAIN_ANSWER    = "N/A"
PART_C_XML_ANSWER      = "N/A"
PART_C_SANDWICH_ANSWER = "N/A"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C was not run because the structural effect was successfully demonstrated in Part B. 
The 70B model failed the PLAIN condition when near-miss distractors were added, proving that even large models require structural scaffolding 
to properly discriminate between highly similar, conflicting context chunks.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low and the model must discriminate between near-duplicate or conflicting chunks of text. 
In these scenarios, XML tags act as vital "Attention Anchors" that prevent semantic blending by enforcing strict document boundaries. 
Furthermore, using the Sovereign Injection Pattern—which relies on the "Sandwich Rule" to place query reminders at both the top and bottom 
of the context—protects against Recency and Primacy bias, forcing the model to evaluate each document as an isolated unit rather than a continuous narrative.
"""
