import json
import Models

def execute_function_call(message,client):
    function_name = message.tool_calls[0].function.name
    arguments = message.tool_calls[0].function.arguments

    match function_name:
        case "save_place":
            results = save_place(arguments)
        case "create_place":
            results = create_place(arguments,client)
        case "modify_place":
            results = modify_place(arguments,client)
        case "create_character":
            results = create_character(arguments,client)
        case "modify_character":
            results = modify_character(arguments,client)
        case "create_other":
            results = create_other(arguments,client)
        case "modify_other":
            results = modify_other(arguments,client)
        case _:
            results = f"Error: function {function_name} does not exist"

    return results


def save_place(content):
    """
    Saves the newly created place.

    Args:
        name (str): The name of the place.
        summary (str): A summary of the place.
        detailed (str): A detailed description of the place.
        region (str): The region in which the place is located.
        population (int): The population of the place.

    Returns:
        str: A success message if the content is successfully saved, or an error message if saving fails.
    """
    name = json.loads(content)['name'].replace(" ", "_")
    try:
        with open(f'campaign/places/{name}.txt', 'w') as file:
            file.write(content)
        return f"Successfully saved content to campaign/places/{name}.txt"
    except Exception as e:
        return f"Failed to save content: {str(e)}"

def create_place(content,client):
    """
    Dispatch the user to the place creation model.

    Args:
        content (str): The user query.
    """
    Models.call_create_place_model(content,client)
    return "create_place function"


def modify_place(content,client):
    """
    Dispatch the user to the place modification model.

    Args:
        content (str): The user query.
    """
    Models.call_modify_place_model(content,client)
    return "modify_place function"


def create_character(content,client):
    """
    Dispatch the user to the character creation model.

    Args:
        content (str): The user query.
    """
    Models.call_create_character_model(content,client)
    return "create_character function"


def modify_character(content,client):
    """
    Dispatch the user to the character modification model.

    Args:
        content (str): The user query.
    """
    Models.call_modify_character_model(content,client)
    return "modify_character function"  


def create_other(content,client):
    """
    Dispatch the user to the other creation model.

    Args:
        content (str): The user query.
    """
    Models.call_create_other_model(content,client)
    return "create_other function" 


def modify_other(content,client):
    """
    Dispatch the user to the other modification model.

    Args:
        content (str): The user query.
    """
    Models.call_modify_other_model(content,client)
    return "modify_other function"

def set_place_creation_custom_tools():
    custom_tools= []

    """
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'save_place',
             'description': 'Saves the newly created place. Only use when the user asks to save the place.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the place'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the place'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the place'
                     },
                     'region': {
                         'type': 'string',
                         'description': 'The region in which the place is located.'
                     },
                     'population': {
                         'type': 'string',
                         'description': 'The population of the place.'
                     }
                 }
             },
             "required": ["name", "summary", "detailed", "region", "population"],
         }
         }
    )
    """
    
    return custom_tools

def set_place_modification_custom_tools():
    custom_tools= []

    """
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'save_place',
             'description': 'Saves the newly modified place.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the place'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the place'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the place'
                     },
                     'region': {
                         'type': 'string',
                         'description': 'The region in which the place is located.'
                     },
                     'population': {
                         'type': 'string',
                         'description': 'The population of the place.'
                     }
                 }
             },
             "required": ["name", "summary", "detailed", "region", "population"],
         }
         }
    )
    """
    
    return custom_tools

def set_character_creation_custom_tools():
    custom_tools= []

    """
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'save_character',
             'description': 'Saves the newly created character.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the character'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the character'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the character'
                     },
                     'race': {
                         'type': 'string',
                         'description': 'The race of the character.'
                     },
                     'sex': {
                         'type': 'string',
                         'description': 'The sex of the character.'
                     }
                 }
             },
             "required": ["name", "summary", "detailed", "race", "sex"],
         }
         }
    )
    """

    return custom_tools

def set_character_modification_custom_tools():
    custom_tools= []

    """
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'save_character',
             'description': 'Saves the newly modified character.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the character'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the character'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the character'
                     },
                     'race': {
                         'type': 'string',
                         'description': 'The race of the character.'
                     },
                     'sex': {
                         'type': 'string',
                         'description': 'The sex of the character.'
                     }
                 }
             },
             "required": ["name", "summary", "detailed", "race", "sex"],
         }
         }
    )
    """

    return custom_tools

def set_dispatch_custom_tools():
    custom_tools = []

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'create_place',
             'description': 'Dispatch the user to the place creation model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'modify_place',
             'description': 'Dispatch the user to the place modification model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'create_character',
             'description': 'Dispatch the user to the character creation model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'modify_character',
             'description': 'Dispatch the user to the character modification model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'create_other',
             'description': 'Dispatch the user to the other creation model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'modify_other',
             'description': 'Dispatch the user to the other modification model.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'userQuery': {
                         'type': 'string',
                         'description': 'A copy of the user query.'
                     }
                 }
             },
             "required": ["userQuery"],
         }
         }
    )

    return custom_tools

def set_custom_tools():
    custom_tools = []

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'save_content',
             'description': 'Saves the newly created content.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the place'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the place'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the place'
                     },
                     'region': {
                         'type': 'string',
                         'description': 'The region in which the place is located.'
                     },
                     'population': {
                         'type': 'string',
                         'description': 'The population of the place.'
                     },
                     "saving": {
                         "type": "string",
                         "enum": ["save", "don't save"],
                         "description": "If the user asked to save.",
                     },
                 }
             },
             "required": ["name", "summary", "detailed", "region", "population", "saving"],
         }
         }
    )


    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'create_character',
             'description': 'Creates a new character.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the character'
                     },
                     'age': {
                         'type': 'integer',
                         'description': 'Age of the character'
                     },
                     'gender': {
                         'type': 'string',
                         'description': 'Gender of the character'
                     },
                     'occupation': {
                         'type': 'string',
                         'description': 'Occupation of the character'
                     },
                 }
             },
             "required": ["name", "age", "gender", "occupation"],
         }
         }
    )


    return custom_tools