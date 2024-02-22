import os
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
import custom_tools as ct
import utils

def set_openai_api_clients():
    load_dotenv(override=True)  # Load environment variables from .env file
    openai_api_key =  os.getenv("OPENAI_API_KEY")

    clients = {
        "placeCreateClient": OpenAI(api_key=openai_api_key),
        "placeModifyClient": OpenAI(api_key=openai_api_key),
        "characterCreateClient": OpenAI(api_key=openai_api_key),
        "characterModifyClient": OpenAI(api_key=openai_api_key),
        "otherCreateClient": OpenAI(api_key=openai_api_key),
        "otherModifyClient": OpenAI(api_key=openai_api_key),
        "dispatchRoleClient": OpenAI(api_key=openai_api_key)
    }

    return clients


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(client, messages, tools=None, tool_choice=None):

    model = "gpt-3.5-turbo-0613"

    # Count the tokens of the conversation
    tokenNumber = utils.num_tokens_from_messages(messages, model)
    print(f"Number of tokens: {tokenNumber}")
    while tokenNumber > 2000:
        # Pruning the conversation
        print("Pruning the conversation")
        messages = utils.prune_messages(messages)
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

def call_dispatch_model(userQuery, clients, messages):

    # Add user query to messages
    messages.append({"role": "user", "content": userQuery})

    # Set up custom tools
    custom_tools = ct.set_dispatch_custom_tools()

    # Call OpenAI API
    response = chat_completion_request(
        clients.get('dispatchRoleClient'), messages, tools=custom_tools, tool_choice='auto'
    )

    # Handle the response
    handleAssistantResponse(response, messages, clients.get('dispatchRoleClient'))

    return messages

def call_create_place_model(content, placeCreateClient):

    # Extract userQuery and upperRegion from content
    data = eval(content)
    userQuery = data.get("userQuery")
    upperRegion = data.get("upperRegion")

    print("create_place function")

    # Load properties from prompt.ini
    config = utils.get_properties()

    # Write the system prompt for place creation
    createPlaceSystemPrompt = config.get('section2','system.prompt.place.creation')
    messages=[
            {"role": "system", "content": createPlaceSystemPrompt}
        ]
    
    if upperRegion is None:
        upperRegion = input("Does this new place need to exist in an existing region (which one) ? : ")

    # List all the places
    places = utils.list_places()

    # Search refered place in all places
    existingPlaces = utils.findExistingPlace(upperRegion, places)

    # Add upper region context to content
    if existingPlaces:
        userQuery = utils.addUpperRegionToContext(userQuery, existingPlaces)
    
    
    # Add user query to messages
    messages.append({"role": "user", "content": userQuery})

    # Set up custom tools
    custom_tools = ct.set_place_creation_custom_tools()
    
    # Loop for place creation
    while True:
        # Call OpenAI API
        response = chat_completion_request(
            placeCreateClient, messages, tools=custom_tools, tool_choice={"type": "function", "function": {"name": "write_place"}}
        )
    
        # Handle the response
        handleAssistantResponse(response, messages, placeCreateClient)
    
        # Print conversation so far
        utils.pretty_print_conversation(messages,"default")

        # Ask for user input in place creation
        userQuery = input("You: ")
        if userQuery == 'quit':
            print("place creation exited")
            break
        elif userQuery == 'save':
            userQuery = utils.saveCurrentPlace(messages)
            break

        # Add user query to messages
        messages.append({"role": "user", "content": userQuery})

    return "create_place function"

def call_modify_place_model(content, placeModifyClient):

    # Extract userQuery and upperRegion from content
    data = eval(content)
    userQuery = data.get("userQuery")
    to_modify = data.get("to_modify")

    print("modify_place function")
    
    # Load properties from prompt.ini
    config = utils.get_properties()
    
    # Write the system prompt for place modification
    modifyPlaceSystemPrompt = config.get('section2','system.prompt.place.modification')
    messages=[
            {"role": "system", "content": modifyPlaceSystemPrompt}
        ]
    
    # List all the places
    places = utils.list_places()

    # Search refered place in all places
    existingPlaces = utils.findExistingPlace(to_modify, places)

    # Add the existing place context to the user query
    if existingPlaces:
        userQuery = utils.addPlaceToModifyToContext(userQuery, existingPlaces)

    # Add user query to messages
    messages.append({"role": "user", "content": userQuery})

    # Set up custom tools
    custom_tools = ct.set_place_modification_custom_tools()

    # Loop for place modification
    while True:

        # Call OpenAI API
        response = chat_completion_request(
            placeModifyClient, messages, tools=custom_tools, tool_choice={"type": "function", "function": {"name": "write_place"}}
        )
    
        # Handle the response
        handleAssistantResponse(response, messages, placeModifyClient)
    
        # Print conversation so far
        utils.pretty_print_conversation(messages,"default")

        # Ask for user input in place modification
        userQuery = input("You: ")
        if userQuery == 'quit':
            print("place modification exited")
            break
        elif userQuery == 'save':
            userQuery = utils.saveCurrentPlace(messages)
            break

        # Add user query to messages
        messages.append({"role": "user", "content": userQuery})

    return "modify_place function"

def call_create_character_model(userQuery, characterCreateClient):

    print("create_character function")

    # Load properties from prompt.ini
    config = utils.get_properties()

    # Write the system prompt for character creation
    createCharacterSystemPrompt = config.get('section2','system.prompt.character.creation')
    messages=[
            {"role": "system", "content": createCharacterSystemPrompt}
        ]

    # Add user query to messages
    messages.append({"role": "user", "content": userQuery})

    # Set up custom tools
    custom_tools = ct.set_character_creation_custom_tools()
    
    # Loop for character creation
    while True:
        # Call OpenAI API
        response = chat_completion_request(
            characterCreateClient, messages, tools=custom_tools, tool_choice={"type": "function", "function": {"name": "write_character"}}
        )
    
        # Handle the response
        handleAssistantResponse(response, messages, characterCreateClient)
    
        # Print conversation so far
        utils.pretty_print_conversation(messages,"default")

        # Ask for user input in character creation
        userQuery = input("You: ")
        if userQuery == 'quit':
            print("character creation exited")
            break
        elif userQuery == 'save':
            userQuery = utils.saveCurrentCharacter(messages)
            print("character creation exited")
            break

        # Add user query to messages
        messages.append({"role": "user", "content": userQuery})

    return "create_character function"

def call_modify_character_model(content, characterModifyClient):
    
    print("modify_character function")

    # Extract userQuery and to_modify from content
    data = eval(content)
    userQuery = data.get("userQuery")
    to_modify = data.get("to_modify")

    # Load properties from prompt.ini
    config = utils.get_properties()

    # Write the system prompt for character modification
    modifyCharacterSystemPrompt = config.get('section2','system.prompt.character.modification')
    messages=[
            {"role": "system", "content": modifyCharacterSystemPrompt}
        ]
    
    # List all the characters
    characters = utils.list_characters()

    # Search refered character in all characters
    existingCharacters = utils.findExistingCharacter(to_modify, characters)

    # Add the existing character context to the user query
    if existingCharacters:
        userQuery = utils.addCharacterToModifyToContext(userQuery, existingCharacters)
    
    # Add user query to messages
    messages.append({"role": "user", "content": userQuery})

    # Set up custom tools
    custom_tools = ct.set_character_modification_custom_tools()

    # Loop for character modification
    while True:
        # Call OpenAI API
        response = chat_completion_request(
            characterModifyClient, messages, tools=custom_tools, tool_choice={"type": "function", "function": {"name": "write_character"}}
        )
    
        # Handle the response
        handleAssistantResponse(response, messages, characterModifyClient)
    
        # Print conversation so far
        utils.pretty_print_conversation(messages,"default")

        # Ask for user input in character modification
        userQuery = input("You: ")
        if userQuery == 'quit':
            print("character modification exited")
            break
        elif userQuery == 'save':
            userQuery = utils.saveCurrentCharacter(messages)
            print("character modification exited")
            break

        # Add user query to messages
        messages.append({"role": "user", "content": userQuery})

    return "modify_character function"


def call_create_other_model():
    print("create_other function")
    return "create_other function"

def call_modify_other_model():
    print("modify_other function")
    return "modify_other function"

def handleAssistantResponse(response, messages,client):
    assistant_message = response.choices[0].message
    if assistant_message.tool_calls:
        assistant_message.content = str(assistant_message.tool_calls[0].function)

    # Call a function if there is one
    messages.append({"role": assistant_message.role, "content": assistant_message.content})
    if assistant_message.tool_calls:
        results = ct.execute_function_call(assistant_message,client)
        messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})

    return messages