import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_FILE = ".env"
GROQ_ENV_KEY = "GROQ_API"
OPENAI_ENV_KEY = "OPENAI_API_KEY"

def read_env_file():
    """Read .env file into a dict if it exists."""
    env_vars = {}
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    return env_vars

def write_env_file(env_vars):
    """Write environment variables back to .env file safely."""
    with open(API_FILE, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

def ensure_api_key(provider="groq"):
    """
    Ensure API key is available for the specified provider:
    - If not present, prompt and append.
    - If present but empty/invalid, re-prompt and replace only that line.
    """
    env_vars = read_env_file()
    
    if provider.lower() == "groq":
        env_key = GROQ_ENV_KEY
        provider_name = "GROQ"
    elif provider.lower() == "openai":
        env_key = OPENAI_ENV_KEY
        provider_name = "OpenAI"
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    api_key = env_vars.get(env_key) or os.getenv(env_key)

    # If key is missing or empty, ask user
    if not api_key:
        api_key = input(f"Enter your {provider_name} API Key: ").strip()
        env_vars[env_key] = api_key
        write_env_file(env_vars)

    return api_key

def get_base_url(provider="groq"):
    """Get the base URL for the specified provider."""
    if provider.lower() == "groq":
        return "https://api.groq.com/openai/v1"
    elif provider.lower() == "openai":
        return "https://api.openai.com/v1"
    else:
        raise ValueError(f"Unsupported provider: {provider}")
