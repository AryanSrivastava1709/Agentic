from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# llm model
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = model.invoke(state.get("messages"))
    return {"messages": [response]}


def Sample(state: State):
    print("\n\nInside sample node", state)
    return {"messages": ["Sample message appended"]}


graph_builder = StateGraph(State)


# These are the nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", Sample)

# These are the edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, My name is Piyush Garg"]}))
print("\n\nUpdated State", updated_state)
