import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

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
    )

    user_prompt = args.user_prompt

    if not response.usage:
        raise RuntimeError("response.usage object not found")
    
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")        
    
    return response.choices[0].message.content

def main():
    api_key = load_api_key()
    
    parser = build_parser()
    args = parser.parse_args()

    client = build_client(api_key)

    messages: list[dict[str, object]] = [
    {"role": "user", "content": args.user_prompt},
    ]

    content = generate_content(client, messages, args)
    print(content)

if __name__ == "__main__":
    main()