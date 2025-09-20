from dotenv import load_dotenv
from openai import OpenAI
import requests
import json

load_dotenv()
client = OpenAI()

def get_weather(city : str):
    print("🛠️ Tool called : get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

    return "Something went wrong"

available_tools={
    "get_weather":{
        "fn": get_weather,
        "description":"Takes a city name as input and return the current weather of the city"
    }
}

system_prompt = f"""
    You are a helpful AI assiatant who is soecialized is resolving users queries. 
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan step by step execution, based on the planning,
    select the relevant tool from the available tools. and based on the tool selection you perform an action to call the tool.
    Wait for the tool to return the observation and based on the observation you resolve the user query.

    Rules:
    - Follow the output json format
    - Always perform one step at a time and wait from next input
    - Carefully analyse the user query

    Output json format:
    {{
        "step" : "string",
        "content: : "string",
        "function" : "the name of the function if the step is action",
        "input" : "the input parameter for the function",
    }}

    Available tools:
    - get_weather: Takes a city name as input and return the current weather of the city.

    Example:
    User Query: What is the current weather of new york?
    Output:{{"step":"plan", "content":"The user is interested in weather data of new york."}}
    Output:{{"step":"plan", "content":"From the available tools I should call get_weather"}}
    Output:{{"step":"action", "function":"get_weather", "input":"new york"}}
    Output:{{"step":"observe", "output":"12 degree Cel"}}
    Output:{{"step":"output", "content":"The weather for the new york is 12 degrees."}}
"""
messages = [
        {
            "role":"system",
            "content": system_prompt,
        },
]
user_query = input('> ')
messages.append({"role":"user", "content": user_query})
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parserd_output = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parserd_output)})

    if parserd_output.get("step") == "plan":
        print(f"🧠: {parserd_output.get('content')}")
        continue
    if parserd_output.get("step") == "action":
        tool_name = parserd_output.get("function")
        tool_input = parserd_output.get("input")

        if available_tools.get(tool_name, False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
            continue
    if parserd_output.get("step") == "output":
        print(f"🤖: {parserd_output.get('content')}")
        break

# response = client.chat.completions.create(
#     model="gpt-4o",
#     response_format={"type":"json_object"},
#     messages=[
#         {
#             "role":"system",
#             "content": system_prompt,
#         },
#         {
#             "role": "user",
#             "content": "What is the current weather of new york?",
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps({"step":"plan", "content":"The user is interested in weather data of new york."})
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps({"step":"plan", "content":"From the available tools I should call get_weather"})
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps({"step": "action", "function": "get_weather", "input": "new york"})
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps({"step": "observe", "output": "31 degree celcius"})
#         },
#     ]
# )

# print(response.choices[0].message.content)