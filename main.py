import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from AI_instructions import system_prompt
from AI_instructions import available_functions
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key was not found. ☠")
    
    parser = argparse.ArgumentParser(description="Beregond")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("API request failed. ☠")
        
        if response.function_calls:
            results_list = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception('Error: function call result was not found')
                if not function_call_result.parts[0].function_response:
                    raise Exception('Error: function call result is not a function response')
                if not function_call_result.parts[0].function_response.response:
                    raise Exception('Error: function call result does not contain data')
                
                results_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=results_list))

        else:
            if not response:
                print("Alas! The enemy assailed me and I was forced to retreat. I could not complete the task in the alotted time.")
                raise SystemExit(1)
            if args.verbose:
                print(f"My captain's orders: {args.user_prompt}")
                print(f"Gold spent by the captain: {response.usage_metadata.prompt_token_count}")
                print(f"Gold spent by Beregond: {response.usage_metadata.candidates_token_count}")
            print("By your command!")
            print(response.text)
            return

if __name__ == "__main__":
    main()
