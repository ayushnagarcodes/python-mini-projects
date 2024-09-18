from dotenv import load_dotenv
from openai import OpenAI
import sys
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
MODEL = {"name": "gpt-4o-mini", "model_costs": {"input_cost": 0.00015 / 1000, "output_cost": 0.0006 / 1000}}


def exit_chat():
    sys.exit(0)


def calculate_tokens_cost(chat_completion):
    input_tokens_cost = chat_completion.usage.prompt_tokens * MODEL["model_costs"]["input_cost"]
    output_tokens_cost = chat_completion.usage.completion_tokens * MODEL["model_costs"]["output_cost"]
    return input_tokens_cost + output_tokens_cost


def get_chat_completion(messages):
    chat_completion = client.chat.completions.create(
        model=MODEL["name"],
        messages=messages,
        temperature=0.7,
        tools=functions_list,
        tool_choice="auto",
    )
    return chat_completion


def converse(messages):
    while True:
        prompt = input("Enter a message: ")
        messages.append({"role": "user", "content": prompt})

        chat_completion = get_chat_completion(messages)
        assistant_message = chat_completion.choices[0].message
        messages.append(assistant_message)

        tool_call = None
        function_name = None
        if assistant_message.tool_calls: tool_call = assistant_message.tool_calls[0]
        if tool_call: function_name = tool_call.function.name

        cost = calculate_tokens_cost(chat_completion)

        if tool_call: print(tool_call.id)
        print(f"You: {prompt}")
        print(f"Assistant: {assistant_message.content}")
        print(f"Cost: ${cost:.10f}\n")
        if function_name: function_mapping[function_name]()


function_mapping = {
    "exit_chat": exit_chat
}

functions_list = [
    {
        "type": "function",
        "function": {
            "name": "exit_chat",
            "description": "Exit chat to end conversation",
        },
    }
]

messageHistory = []

converse(messageHistory)
