import json

def execute_function_call(message):
    if message.tool_calls[0].function.name == "save_content":
        results = save_content(message.tool_calls[0].function.arguments)
    else:
        results = f"Error: function {message.tool_calls[0].function.name} does not exist"
    return results


def save_content(content):
    """
    Saves the newly created content.

    Args:
        name (str): The name of the place.
        summary (str): A summary of the place.
        detailed (str): A detailed description of the place.
        region (str): The region in which the place is located.
        population (int): The population of the place.
        saving (str): If the user asked to save.    

    Returns:
        str: A success message if the content is successfully saved, or an error message if saving fails.
    """
    name = json.loads(content)['name'].replace(" ", "_")
    saving = json.loads(content)['saving']
    if saving == "don't save":
        return "Content not saved"
    else:
        try:
            with open(f'campaign/places/{name}.txt', 'w') as file:
                file.write(content)
            return f"Successfully saved content to campaign/places/{name}.txt"
        except Exception as e:
            return f"Failed to save content: {str(e)}"
    

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

    return custom_tools