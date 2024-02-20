
from openai import OpenAI
from Models import set_openai_api_clients, call_dispatch_model
import utils

client = OpenAI()
GPT_MODEL = "gpt-3.5-turbo-0613"


def main():

    # Load properties from prompt.ini
    config = utils.get_properties()

    # Set up OpenAI client
    clients = set_openai_api_clients()

    # We setup the first model whose role is to dispatch the user's query to the right tool
    # dispatch prompt
    systemPrompt = config.get('section2','system.prompt.dispatch')
    messages=[
            {"role": "system", "content": systemPrompt}
        ]

    # Main loop
    while True:

        # Ask for user input
        userQuery = input("You: ")
        if userQuery == 'quit':
            break

        messages = call_dispatch_model(userQuery, clients, messages)

        # Print conversation so far
        utils.pretty_print_conversation(messages)


if __name__ == "__main__":
    main()