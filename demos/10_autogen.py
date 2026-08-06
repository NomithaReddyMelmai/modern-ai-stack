"""
DEMO 10 — AutoGen (Microsoft): conversational multi-agent (writer <-> critic).

Run:  python demos/10_autogen.py

Talking point: AutoGen frames multi-agent work as an async *conversation* between
agents until a termination condition. Here a writer and a critic iterate on a
tagline until the critic says APPROVE. Note `model_info` — required to use a
non-OpenAI model (Claude via OpenRouter) with the OpenAI-compatible client.
"""
import sys, os, asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import FAST_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL, assert_key

assert_key()

model_client = OpenAIChatCompletionClient(
    model=FAST_MODEL,
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    model_info={                       # required for non-OpenAI models
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
        "structured_output": False,
    },
)

async def main():
    writer = AssistantAgent(
        "writer", model_client=model_client,
        system_message="You write punchy product taglines. Revise on feedback.",
    )
    critic = AssistantAgent(
        "critic", model_client=model_client,
        system_message="Critique the tagline in one line. Reply with the single "
                       "word APPROVE (and nothing else) once it is excellent.",
    )
    team = RoundRobinGroupChat(
        [writer, critic],
        termination_condition=TextMentionTermination("APPROVE") | MaxMessageTermination(8),
    )
    await Console(team.run_stream(task="A tagline for the Acme Sentinel security robot."))
    await model_client.close()

asyncio.run(main())
