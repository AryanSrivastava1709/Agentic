from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
import os

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are an expert evaluator.

Your task is to evaluate how well the given answer responds to the user's question.

Score the answer on a scale from 1 to 10 using the following criteria:
- Correctness
- Completeness
- Relevance
- Clarity
- Helpfulness

Scoring Guide:
- 10: Perfect answer. Completely correct, complete, clear, and directly answers the question.
- 8-9: Very good answer with only minor omissions or imperfections.
- 6-7: Mostly correct but missing important details or explanations.
- 4-5: Partially correct but contains significant gaps or inaccuracies.
- 2-3: Mostly incorrect or largely irrelevant.
- 1: Completely incorrect, irrelevant, or no meaningful answer.

Return ONLY the score as a single integer.
Do not explain your reasoning.
Do not return any other text.

Example 1:

Question:
What is the capital of France?

Answer:
Paris is the capital of France.

Output:
10

Example 2:

Question:
What is the capital of France?

Answer:
I think it is London.

Output:
1

Example 3:

Question:
Explain what Python decorators are.

Answer:
Decorators allow you to modify the behavior of functions without changing their source code by wrapping them inside another function.

Output:
9
"""

load_dotenv()

# llm mode
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)


# state initialization
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


# graph
graph_builder = StateGraph(State)


# nodes - for chatbots
def chatbot_3_1_flashlite(state: State):
    print("\n\n ChatBot 1 Node", state)
    responses = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[{"role": "user", "content": state.get("user_query")}],
    )

    state["llm_output"] = responses.choices[0].message.content
    return state


def chatbot_3_5_flash(state: State):
    print("\n\n ChatBot 2 Node", state)
    responses = client.chat.completions.create(
        model="gemini-3.5-flash",
        messages=[{"role": "user", "content": state.get("user_query")}],
    )

    state["llm_output"] = responses.choices[0].message.content
    return state


def endnode(state: State):
    print("\n\n End Node", state)
    return state


# nodes - for evaluation
def evaluate_response(state: State) -> Literal["chatbot_3_5_flash", "endnode"]:
    print("\n\n Evaluate Node", state)

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Question:
{state.get("user_query")}

Answer:
{state.get("llm_output")}
""",
            },
        ],
    )

    score = int(response.choices[0].message.content)
    print("SCORE: ", score, "\n\n")

    if score >= 8:
        return "endnode"

    return "chatbot_3_5_flash"


# building the edges and nodes
graph_builder.add_node("chatbot_3_1_flashlite", chatbot_3_1_flashlite)
graph_builder.add_node("chatbot_3_5_flash", chatbot_3_5_flash)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot_3_1_flashlite")
graph_builder.add_conditional_edges("chatbot_3_1_flashlite", evaluate_response)
graph_builder.add_edge("chatbot_3_5_flash", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

# building the graph
user_query = input("Please input your query: -> ")
updated_state = graph.invoke(State({"user_query": user_query}))

print("\n\nUpdated State", updated_state)
