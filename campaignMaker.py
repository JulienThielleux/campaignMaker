import os
from dotenv import load_dotenv
import configparser
from openai import OpenAI
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt

from custom_functions import execute_function_call, set_custom_tools
import utils

client = OpenAI()
GPT_MODEL = "gpt-3.5-turbo-0613"

# Load properties from prompt.ini
def get_properties():
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read('prompt.ini')

# Set up OpenAI API key
def set_openai_api_key():
    load_dotenv()  # Load environment variables from .env file
    return os.getenv("OPENAI_API_KEY")

def call_openai_api():

    # Set up OpenAI client
    client = OpenAI(api_key=set_openai_api_key())

    # Initial prompt
    systemPrompt = CONFIG.get('section1','place.creation.noContext')
    messages=[
            {"role": "system", "content": systemPrompt}
        ]
    
    # Set up custom tools
    custom_tools = set_custom_tools()

    # Main loop
    while True:

        userQuery = input("You: ")
        if userQuery == 'quit':
            break

        # List all the existing pieces of lore
        places = get_existing_lore()

        # Check if there is existing lore matching the user query
        existingPlaceContext = setExistingPlaceContext(userQuery, places)
        if existingPlaceContext:
            userQuery = update_query_with_context(userQuery, existingPlaceContext)
        
        # Add user query to messages
        messages.append({"role": "user", "content": userQuery})

        # Call OpenAI API
        response = chat_completion_request(
            messages, tools=custom_tools, tool_choice='auto'
        )

        assistant_message = response.choices[0].message
        if assistant_message.tool_calls:
            assistant_message.content = str(assistant_message.tool_calls[0].function)

        messages.append({"role": assistant_message.role, "content": assistant_message.content})
        if assistant_message.tool_calls:
            results = execute_function_call(assistant_message)
            messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})

        utils.pretty_print_conversation(messages)

def get_existing_lore():
    places = {}

    for root, dirs, files in os.walk('campaign'):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    file_content = json.load(file)
                    name = file_content['name']
                    summary = file_content['summary']
                    places[name] = summary

    return places       

def setExistingPlaceContext(userQuery, places):
    existingPlaceContext = []
    for place in places:
        if place.lower() in userQuery.lower():
            existingPlaceContext.append(places[place])
            print(place, places[place])

    return existingPlaceContext

def update_query_with_context(userQuery, existingPlaceContext):
    updatedUserQuery = userQuery + '\n' + CONFIG.get('section1','place.creation.withContext') + '\n'
    for context in existingPlaceContext:
        updatedUserQuery = updatedUserQuery + f'{context}\n'
    return updatedUserQuery

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):

    # Count the tokens of the conversation
    tokenNumber = utils.num_tokens_from_messages(messages, model)
    print(f"Number of tokens: {tokenNumber}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def main():
    get_properties()
    call_openai_api()

if __name__ == "__main__":
    main()