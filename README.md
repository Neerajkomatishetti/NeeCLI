# NeeCLI

A command-line interface (CLI) tool for chatting with Large Language Models (LLMs) using Groq and OpenAI APIs.

## Features

- **Multi-provider support**: Chat with Groq and OpenAI models
- **Interactive chat loop**: Continuous conversation mode
- **Conversation history**: Save and load chat history
- **Streaming responses**: Real-time response streaming
- **Flexible model selection**: Choose from different LLM models
- **Environment-based configuration**: Secure API key management

## Installation

### Prerequisites

- Python 3.8 or higher
- A Groq or OpenAI API key

### Install the package

```bash
# Clone the repository
git clone <repository-url>
cd NeeCLI

# Install dependencies
pip install -e .
```

## Configuration

### API Keys

You can set your API keys in several ways:

1. **Environment variables**:
   ```bash
   export GROQ_API="your-groq-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. **`.env` file** (recommended):
   ```bash
   GROQ_API=your-groq-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

3. **Interactive prompt**: The tool will prompt you for the API key if not found.

## Usage

### Basic Commands

```bash
# Send a single message
neecli chat "Hello, how are you?"

# Start an interactive chat loop
neecli loop "Let's start a conversation"

# View conversation history
neecli history

# Clear conversation history
neecli clear
```

### Advanced Options

```bash
# Use a specific model
neecli chat "Explain quantum computing" --model "openai/gpt-oss-20b"

# Adjust response randomness
neecli chat "Tell me a story" --temperature 0.9

# Use OpenAI instead of Groq
neecli chat "Hello" --provider openai --model "gpt-3.5-turbo"

# Interactive loop with custom settings
neecli loop "Start a coding session" --model "openai/gpt-oss-20b" --temperature 0.3 --provider groq
```

### Interactive Chat Loop

When using the `loop` command, you can:

- Type your messages and press Enter
- Type `exit` to quit the chat loop
- Type `clear` to clear conversation history
- The conversation automatically clears after 20 messages to prevent context overflow

## Available Models

### Groq Models
- `openai/gpt-oss-20b` (default)
- `llama3-8b-8192`
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

### OpenAI Models
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`

## Development

### Project Structure

```
NeeCLI/
├── NeeCLI/
│   ├── __init__.py
│   ├── cli.py          # Main CLI implementation
│   ├── config.py       # Configuration and API key management
│   ├── history.py      # Conversation history management
│   └── main.py         # Entry point
├── tests/
│   └── test_cli.py     # Test suite
├── pyproject.toml      # Project configuration
└── README.md
```

### Running Tests

```bash
python -m pytest tests/
```

### Building the Package

```bash
python -m build
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**: Make sure your API key is set in environment variables or `.env` file
2. **Model Not Available**: Check if the model name is correct for your provider
3. **Rate Limiting**: Some models have rate limits; try again later
4. **Network Issues**: Check your internet connection

### Error Messages

- `Failed to initialize client`: Check your API key and internet connection
- `Model not found`: Verify the model name is correct for your provider
- `Rate limit exceeded`: Wait before making more requests

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.

