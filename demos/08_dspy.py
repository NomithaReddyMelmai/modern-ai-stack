"""
DEMO 8 — DSPy: program your prompts, then let an OPTIMIZER write them for you.

Run:  python demos/08_dspy.py   (makes several LLM calls during compile)

Talking point: stop hand-tuning prompt strings. In DSPy you declare the I/O
(a Signature) and a strategy (ChainOfThought), then a teleprompter compiles
few-shot demos / instructions automatically against a metric. Prompts become
artifacts you optimize, not guess.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dspy
from config import SMART_MODEL_LITELLM, OPENROUTER_API_KEY, assert_key

assert_key()
dspy.configure(lm=dspy.LM(SMART_MODEL_LITELLM, api_key=OPENROUTER_API_KEY))

class QA(dspy.Signature):
    """Answer with ONLY the final number, no words."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

program = dspy.ChainOfThought(QA)
print("\n--- Before optimization ---")
print(program(question="A robot travels 12 km in 4 hours. Speed in km/h?").answer)

# Tiny labeled set + a metric; the optimizer bootstraps good few-shot demos.
trainset = [
    dspy.Example(question="6 units at $3 each. Total?", answer="18").with_inputs("question"),
    dspy.Example(question="A tank holds 20L, 5L used. Left?", answer="15").with_inputs("question"),
    dspy.Example(question="3 robots, 4 arms each. Arms?", answer="12").with_inputs("question"),
]
metric = lambda ex, pred, trace=None: ex.answer.strip() == pred.answer.strip()

optimized = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=2).compile(
    dspy.ChainOfThought(QA), trainset=trainset
)
print("\n--- After optimization ---")
print(optimized(question="A robot travels 12 km in 4 hours. Speed in km/h?").answer)

# Show the auto-generated few-shot demos DSPy attached to the prompt:
dspy.inspect_history(n=1)
