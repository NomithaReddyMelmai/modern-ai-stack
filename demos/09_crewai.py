"""
DEMO 9 — CrewAI: role-based multi-agent collaboration (a "crew" with a process).

Run:  python demos/09_crewai.py

Talking point: CrewAI models a team — each agent has a role/goal/backstory and
tasks flow between them (sequential or hierarchical). Great mental model for
"researcher -> writer -> reviewer" style pipelines. Uses LiteLLM, so OpenRouter
is just the `openrouter/` prefix.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent, Task, Crew, Process, LLM
from config import FAST_MODEL_LITELLM, OPENROUTER_API_KEY, assert_key

assert_key()
llm = LLM(model=FAST_MODEL_LITELLM, api_key=OPENROUTER_API_KEY)

researcher = Agent(
    role="Market Analyst",
    goal="Identify 3 concrete use cases for warehouse robots",
    backstory="You spot practical, ROI-driven applications quickly.",
    llm=llm, verbose=True,
)
writer = Agent(
    role="Technical Writer",
    goal="Turn findings into a crisp 4-bullet executive summary",
    backstory="You write for busy execs — clear and jargon-free.",
    llm=llm, verbose=True,
)

research = Task(
    description="List 3 high-ROI use cases for the Acme Hauler warehouse robot.",
    expected_output="Three bullet points, each with a one-line ROI rationale.",
    agent=researcher,
)
summarize = Task(
    description="Write a 4-bullet executive summary from the research.",
    expected_output="Exactly four punchy bullets.",
    agent=writer, context=[research],
)

crew = Crew(agents=[researcher, writer], tasks=[research, summarize],
            process=Process.sequential, verbose=True)
print("\n=== FINAL ===\n", crew.kickoff())
