import os 
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None: 
        raise RuntimeError("api_key was not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )      
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
            ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions
            )

        if response.usage is None:
            raise RuntimeError("Response usage not found")

        user_prompt = args.user_prompt
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens


        if args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        print("Response:")
        
        
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)

                if not result_message["content"]:
                    raise Exception("Resulting tool message is empty")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(response.choices[0].message.content)
            break
    else:
        print("The maximum number of iterations has been reached.")
        sys.exit(1)

if __name__ == "__main__":
    main()
