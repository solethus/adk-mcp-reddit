# ADK MCP Reddit

A Reddit scout agent built with Google's Agent Development Kit (ADK) that fetches hot posts from subreddits using an external MCP Reddit tool.

## Overview

This project demonstrates how to create an AI agent that can interact with Reddit through a Model-Code-Process (MCP) server. The agent can fetch hot posts from any subreddit and present them to the user.

## Features

- Asynchronous connection to an MCP Reddit server
- Fetches hot posts from specified subreddits
- Configurable post limit
- Graceful error handling for missing dependencies

## Prerequisites

- Python 3.12 or higher
- `uvx` command-line tool (`pip install uvx`)
- Google ADK API key (set in `.env` file)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/solethus/adk-mcp-reddit.git
   cd adk-mcp-reddit
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. Create a `.env` file in the root directory with your Google ADK API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

checkout the agents directory
```bash
cd agents
```

To run the agent with the web ui:
```bash
adk web
```

The agent will:
1. Connect to the MCP Reddit server using `uvx`
2. Discover the available Reddit tools
3. Allow you to interact with the agent to fetch hot posts from subreddits

Example prompts:
- "Show me hot posts from r/gamedev"
- "What's trending on the unity3d subreddit?"
- "Get the top 5 posts from r/unrealengine"

## Project Structure

- `agents/async_reddit_scout/` - Contains the Reddit scout agent implementation
  - `agent.py` - Main agent implementation with MCP tool integration
- `pyproject.toml` - Project dependencies and metadata

## Dependencies

- `google-adk` - Google's Agent Development Kit
- `litellm` - Library for working with language models
- `python-dotenv` - For loading environment variables
- `uvx` - For running the MCP server

## License

See the [LICENSE](LICENSE) file for details.