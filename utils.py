from termcolor import colored
import tiktoken
import configparser
import os
import json


def pretty_print_conversation(messages,mode="default"):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system" and mode != "default":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user" and mode != "default":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def prune_messages(messages):
    # Remove the last message that is not a system message
    for i in range(len(messages)):
        if messages[i]["role"] != "system":
            del messages[i]
            break
    return messages

def list_places():
    places = {}

    for root, dirs, files in os.walk('campaign/places'):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    json_content = json.load(file)
                    name = json_content['name']
                    full_content = json.dumps(json_content)
                    places[name] = full_content

    return places

def list_characters():
    characters = {}

    for root, dirs, files in os.walk('campaign/characters'):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    json_content = json.load(file)
                    name = json_content['name']
                    full_content = json.dumps(json_content)
                    characters[name] = full_content

    return characters

def findExistingPlace(place, knownPlaces):
    existingPlaceContext = []
    for knownPlace in knownPlaces:
        if place.lower() in knownPlace.lower():
            existingPlaceContext.append(knownPlaces[place])
            print(place, knownPlaces[place])
            
    return existingPlaceContext

def findExistingCharacter(character, knownCharacters):
    existingCharacterContext = []
    for knownCharacter in knownCharacters:
        if character.lower() in knownCharacter.lower():
            existingCharacterContext.append(knownCharacters[knownCharacter])
            print(knownCharacter, knownCharacters[knownCharacter])
            
    return existingCharacterContext

def addPlaceToModifyToContext(userQuery, existingPlaceContext):
    updatedUserQuery = userQuery + '\n' + 'to_modify' + '\n'
    for context in existingPlaceContext:
        updatedUserQuery += f'{context}\n'
    return updatedUserQuery

def addUpperRegionToContext(userQuery, existingPlaceContext):
    updatedUserQuery = userQuery + '\n' + 'information on the region in which the place must be created' + '\n'
    for context in existingPlaceContext:
        updatedUserQuery += f'{context}\n'
    return updatedUserQuery

def addCharacterToModifyToContext(userQuery, existingCharacterContext):
    updatedUserQuery = userQuery + '\n' + 'to_modify' + '\n'
    for context in existingCharacterContext:
        updatedUserQuery += f'{context}\n'
    return updatedUserQuery

def saveCurrentPlace(messages):
    # Extract the place name and save.
    content = messages[len(messages)-1]["content"]
    json_content = json.loads(content)
    name = json_content['name']
    name = name.replace(' ', '_')
    name = name.lower()
    placePath = f'campaign/places/{name}.txt'
    # Save the place
    with open(placePath, 'w') as file:
        #write the full json content
        file.write(content)
    return f'Place {name} saved in {placePath}'

def saveCurrentCharacter(messages):
    # Extract the character name and save.
    content = messages[len(messages)-1]["content"]
    json_content = json.loads(content)
    name = json_content['name']
    name = name.replace(' ', '_')
    name = name.lower()
    characterPath = f'campaign/characters/{name}.txt'
    # Save the character
    with open(characterPath, 'w') as file:
        #write the full json content
        file.write(content)
    return f'Character {name} saved in {characterPath}'

# Load properties from prompt.ini
def get_properties():
    config = configparser.ConfigParser()
    config.read('prompt.ini')
    return config