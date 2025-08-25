import click
from openai import OpenAI
from config import ensure_api_key, get_base_url
from history import conversation, save_history, load_history, clear_history

@click.group()
def cli():
    """LLMChat: A CLI to chat with Groq/OpenAI models."""
    """Currently Supports only Groq and OpenAI models.

    --------------------------------------------------
    Type [Commands] --help to get help for Commands"""


    pass

def get_client(provider="groq"):
    """Get OpenAI client for the specified provider."""
    api_key = ensure_api_key(provider)
    base_url = get_base_url(provider)
    
    return OpenAI(
        base_url=base_url,
        api_key=api_key
    )

@cli.command()
@click.argument("message")
@click.option("--model", default="openai/gpt-oss-20b", help="LLM model to use")
@click.option("--temperature", default=0.7, type=float, help="Response randomness (0-1)")
@click.option("--provider", default="groq", type=click.Choice(["groq", "openai"]), help="API provider to use")
def chat(message, model, temperature, provider):
    """Send a single message to the LLM."""
    try:
        client = get_client(provider)
        load_history()
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
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
def history():
    """Show conversation history."""
    load_history()
    if not conversation:
        click.echo("No conversation history.")
        return
    for msg in conversation:
        role = msg["role"].capitalize()
        content = msg["content"]
        click.echo(f"{role}: {content}")

@cli.command()
def clear():
    """Clear conversation history."""
    clear_history()
    click.echo("Conversation history cleared.")

@cli.command()
@click.argument("message", required=True)
@click.option("--model", default="openai/gpt-oss-20b", help="LLM model to use")
@click.option("--temperature", default=0.7, type=float, help="Response randomness (0-1)")
@click.option("--provider", default="groq", type=click.Choice(["groq", "openai"]), help="API provider to use")
def loop(message, model, temperature, provider):
    """Start a continuous interactive chat loop."""
    try:
        client = get_client(provider)
        load_history()
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

        try:
            while True:
                user_input = input("> ").strip()
                if user_input.lower() == "exit":
                    click.echo("Exiting chat loop.")
                    save_history()
                    break

                conversation.append({"role": "user", "content": user_input})
                stream = client.chat.completions.create(
                    model=model,
                    messages=conversation,
                    temperature=temperature,
                    stream=True
                )

                assistant_message = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        assistant_message += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="", flush=True)
                print()
                conversation.append({"role": "assistant", "content": assistant_message})
                save_history()

        except KeyboardInterrupt:
            click.echo("\nExiting chat loop.")
            save_history()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
