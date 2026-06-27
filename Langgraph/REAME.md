# LangGraph Basics with Gemini

This repository demonstrates the fundamentals of building AI workflows using **LangGraph** and **Google Gemini** models.

It contains two examples:

1. **Simple Chatbot Workflow** (`chat.py`)
2. **Conditional Routing Between Multiple LLMs** (`chat2.py`)

---

## Tech Stack

- Python 3.10+
- LangGraph
- LangChain Google GenAI
- Google Gemini API
- OpenAI Python SDK (Gemini OpenAI-compatible endpoint)
- python-dotenv

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/Agentic.git
cd Langgraph
```

Install the required dependencies:

```bash
pip install -U langgraph langchain-google-genai openai python-dotenv
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Example 1 : Simple LangGraph Chatbot (`chat.py`)

This example demonstrates:

- Creating a LangGraph workflow
- Defining a custom state
- Creating nodes
- Connecting nodes using edges
- Calling a Gemini model
- Maintaining conversation history using `add_messages`

### Graph

```text
START
   │
   ▼
Chatbot
   │
   ▼
Sample Node
   │
   ▼
END
```

### Workflow

1. User message enters the graph.
2. Gemini (`gemini-3.1-flash-lite`) generates a response.
3. Response is appended to the state.
4. The workflow proceeds to a sample node.
5. Graph terminates.

---

# Example 2 : Conditional LLM Routing (`chat2.py`)

This example demonstrates an AI workflow where responses are automatically evaluated before deciding whether to use a stronger model.

### Models Used

| Model                 | Purpose                              |
| --------------------- | ------------------------------------ |
| gemini-3.1-flash-lite | Generate the initial answer          |
| gemini-2.5-flash      | Evaluate answer quality              |
| gemini-3.5-flash      | Generate a better answer if required |

---

## Workflow

```text
                 START
                   │
                   ▼
      Gemini 3.1 Flash Lite
                   │
                   ▼
         Evaluate Response
          (Gemini 2.5 Flash)
           │             │
           │             │
      Score >= 8     Score < 8
           │             │
           ▼             ▼
         End        Gemini 3.5 Flash
                           │
                           ▼
                          End
```

---

## Evaluation Strategy

The evaluator checks the generated response based on:

- Correctness
- Completeness
- Relevance
- Clarity
- Helpfulness

The evaluator returns a score between **1–10**.

Routing logic:

- **Score ≥ 8** → End the workflow.
- **Score < 8** → Route the query to Gemini 3.5 Flash for a better answer.

---

## Project Concepts Covered

### LangGraph Basics

- StateGraph
- TypedDict State
- Nodes
- Edges
- START
- END
- Graph Compilation
- Graph Invocation

---

### Conditional Routing

Using

```python
graph_builder.add_conditional_edges(...)
```

to dynamically decide the next node.

---

### LLM-as-a-Judge

Instead of hardcoding decisions, an LLM evaluates another LLM's response and determines whether it is sufficiently good.

This is a common pattern used in production AI systems to reduce costs by:

1. Using a smaller, faster model first.
2. Escalating only difficult queries to a more capable model.

---

## Running the Examples

### Example 1

```bash
python chat.py
```

---

### Example 2

```bash
python chat2.py
```

You will be prompted to enter a query.

Example:

```text
Please input your query:
Explain how the Raft Consensus Algorithm works.
```

The graph will automatically determine whether the initial response is sufficient or whether it should be regenerated using a stronger model.

---

## Learning Outcomes

This project demonstrates:

- Building AI workflows using LangGraph
- Creating custom graph states
- Connecting nodes with edges
- Working with multiple Gemini models
- Conditional graph execution
- LLM-based response evaluation
- Dynamic model routing
- Cost optimization using model escalation
