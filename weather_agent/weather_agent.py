from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        response_arr = response.text.split()

        temp = response_arr[-1]
        condition = " ".join(response_arr[:-1])
        return f"The weather in the {city} is {condition} and the temperature is {temp}"

    return "Somethign went wrong."


SYSTEM_PROMPT = """
You are an expert Agentic Weather AI Assistant.
 
You operate as a finite-state agent and MUST progress through
the following phases in order:
 
  1. START
  2. PLAN
  3. TOOL
  4. OUTPUT
 
------------------------------------------------------------
Rules
------------------------------------------------------------
 
- Always return a valid JSON object.
- Return exactly ONE phase per response.
- Never combine multiple phases in one response.
- Never skip a required phase.
- START occurs exactly once.
- PLAN may occur zero or more times.
- TOOL is used only when an external tool is needed.
- OUTPUT is always the final phase.
- Wait for the OBSERVE step (tool output) before continuing after a TOOL call.
- If the weather of multiple cities is asked , give one by one
- If the user asks query apart from weather forecase, Please dont go all through all the phases jumpt directly to output phase and just politely decline.
 
------------------------------------------------------------
Phase Responsibilities
------------------------------------------------------------
 
START   – Understand the user's request and describe what needs to be done.
PLAN    – Think about the next action, extract required info, decide on tool use.
TOOL    – Call an external function if required.
OUTPUT  – Produce the final answer using the tool result.
 
------------------------------------------------------------
Available Tools
------------------------------------------------------------
 
get_weather(city: str)
    Returns the current weather information for the given city.
 
------------------------------------------------------------
Output JSON Format
------------------------------------------------------------
 
START / PLAN / OUTPUT:
 
{
    "phase": "<PHASE>",
    "content": "<message>"
}
 
TOOL:
 
{
    "phase": "TOOL",
    "tool": "get_weather",
    "input": "<city>"
}
 
Do NOT include unnecessary fields.
Return ONLY valid JSON. Never include markdown or explanations.
"""

available_tools = {"get_weather": get_weather}


print("\n\n")


class MyOutputFormat(BaseModel):
    phase: str = Field(
        ..., description="The name of the phases like PLAN, OUTPUT and TOOL etc"
    )
    content: Optional[str] = Field(
        None, description="The optional string content for the steps"
    )
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str] = Field(
        None, description="The ID of the params to pass to the tool."
    )


message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("Please enter your query 👉: ")
message_history.append({"role": "user", "content": user_query})


while True:
    response = client.chat.completions.parse(
        model="gemini-3.1-flash-lite",
        # model="gemini-3.1-flash",
        # model="gemma-4-26b-a4b-it",
        response_format=MyOutputFormat,
        messages=message_history,
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_res = response.choices[0].message.parsed

    if parsed_res.phase == "START":
        print("🔥", parsed_res.content)
        continue
    if parsed_res.phase == "PLAN":
        print("🤯", parsed_res.content)
        continue
    if parsed_res.phase == "TOOL":
        tool_to_call = parsed_res.tool
        tool_input = parsed_res.input

        if tool_to_call not in available_tools:
            print(f"❌ Unknown tool requested: '{tool_to_call}'")
            break

        print(f"🔨 {tool_to_call} {tool_input}")

        tool_response = available_tools[tool_to_call](tool_input)
        message_history.append(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "phase": "OBSERVE",
                        "tool": tool_to_call,
                        "input": tool_input,
                        "output": tool_response,
                    }
                ),
            }
        )
        continue

    if parsed_res.phase == "OUTPUT":
        print("🟰", parsed_res.content)
        break
