import click
from openai import OpenAI
import os
import json
# from dotenv import load_dotenv

# load_dotenv()
# Initialize OpenAI client with Groq
def create_env(api_k):
    with open(".env", 'w') as file2:
        file2.write(f"GROQ_API={api_k}\n")

try:
    # api_key = os.getenv("GROQ_API")
    API_FILE = '.env'
    if os.path.exists(API_FILE):
        with open(API_FILE, 'r') as f:
            fileLines = f.readlines()
            for line in fileLines:
                if 'GROQ_API' in line:
                    api_content = line.strip()
                    api_key = api_content.split("=")[1]
            if api_key:
                pass
            else:
                api_key = input("Enter your API Key: ")
                with open(".env", 'a') as file:
                    file.write(f"GROQ_API={api_key}\n")

    else:
        api_key = input("Enter your API Key: ")
        create_env(api_key)
            # api_key = input("Enter your API Key: ")
            # create_env(api_key)
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
except Exception as e:
    click.echo(f"Failed to initialize Groq client: {e}", err=True)
    click.echo("Please set the GROQ_API_KEY environment variable.", err=True)
    exit(1)

# Store conversation history
HISTORY_FILE = "chat_history.json"
conversation = []

def save_history():
    """Save conversation history to file."""
    with open(HISTORY_FILE, 'w') as file3:
        json.dump(conversation, file3)

def load_history():
    """Load conversation history from file."""
    global conversation
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            conversation = json.load(f)

@click.group()
def cli():
    """CLI for chatting with an LLM."""
    pass

@cli.command()
@click.argument('message')
@click.option('--model', default='openai/gpt-oss-20b', help='LLM model to use')
@click.option('--temperature', default=0.7, type=float, help='Response randomness (0-1)')
def chat(message, model, temperature):
    """Send a message to the LLM and get a response."""
    try:
        # Load conversation history
        load_history()

        # Add user message to conversation
        conversation.append({"role": "user", "content": message})

        # Call LLM API (non-streaming)
        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=temperature
        )

        # Get assistant response
        assistant_message = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_message})

        # Save conversation history
        save_history()

        # Display response
        click.echo(f"Assistant: {assistant_message}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
def history():
    """Display conversation history."""
    load_history()
    if not conversation:
        click.echo("No conversation history.")
        return
    for msg in conversation:
        role = msg['role'].capitalize()
        content = msg['content']
        click.echo(f"{role}: {content}")

@cli.command()
def clear():
    """Clear conversation history."""
    global conversation
    conversation = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    click.echo("Conversation history cleared.")

@cli.command()
@click.argument('message', required=True)
@click.option('--model', default='openai/gpt-oss-20b', help='LLM model to use')
@click.option('--temperature', default=0.7, type=float, help='Response randomness (0-1)')
def loop(message, model, temperature):
    """Start a continuous chat loop with the LLM. Start with 'llmchat loop \"message\"', then enter prompts directly. Type 'exit' to quit."""

    def clear():
        """Clear conversation history."""
        global conversation
        conversation = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        click.echo("Conversation history cleared.")


    try:
        # Load conversation history
        load_history()

        # Process initial message (non-streaming for simplicity)
        conversation.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=temperature
        )
        assistant_message = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_message})
        save_history()
        click.echo(f"Assistant: {assistant_message}")

        # Enter continuous loop
        while True:
            user_input = input("> ").strip()
            add_input = user_input.split(" ")
            if user_input.lower() == 'exit':
                click.echo("Exiting LLM chat loop.")
                save_history()
                break

            elif add_input[0].lower() == 'add':
                a , b = int(add_input[1]), int(add_input[2])
                def add(a, b):
                    return int(a) + int(b)

                add(a,b)
                print(f"answer: {add(a, b)}")
                conversation.append({"role": "user", "content": user_input})
                continue

            elif user_input:
                conversation.append({"role": "user", "content": user_input})
                # Use streaming for subsequent messages
                stream = client.chat.completions.create(
                    model=model,
                    messages=conversation,
                    temperature=temperature,
                    top_p=1,
                    stop=None,
                    stream=True
                )
                # Collect the full response from the stream
                assistant_message = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        assistant_message += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="", flush=True)
                print()  # New line after streaming
                conversation.append({"role": "assistant", "content": assistant_message})
                save_history()

                count = 0
                if count > 10:
                    clear()
                    print("cleared conversation history")
            else:
                click.echo("Please provide a prompt or type 'exit' to quit.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    cli()