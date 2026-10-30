import os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def load_api_key() -> str | None:
    load_dotenv()
    api_key: str | None = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("openrouter key not found")
    return api_key

def build_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser

def build_client(api_key) -> OpenAI:
    return OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

def generate_content(client, messages, args):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    user_prompt = args.user_prompt

    if not response.usage:
        raise RuntimeError("response.usage object not found")
    
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")        

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception("Error: return tool message is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print(response.choices[0].message.content)
        return True

def main():
    api_key = load_api_key()
    
    parser = build_parser()
    args = parser.parse_args()

    client = build_client(api_key)

    messages: list[dict[str, object]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        if generate_content(client, messages, args):
            break
    else:
        print("Error: the max number of iterations is reached and the model hasn't produced a final response :()")
        exit(1)
        

if __name__ == "__main__":
    main()