import asyncio
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

async def get_tools_async():
    """Connects to the mcp-reddit server via uvx and returns the tools and exit stack."""
    print("--- Attempting to start and connect to mcp-elevenlabs MCP server via uvx ---")
    try:
        # Check if uvx is available (basic check)
        # A more robust check might involve checking the actual command's success
        await asyncio.create_subprocess_shell('uvx --version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uvx',
                args=[ 'elevenlabs-mcp'],
                env={'ELEVENLABS_API_KEY': os.environ.get('ELEVENLABS_API_KEY', '')}
                # Optional: Add environment variables if needed by the MCP server,
                # e.g., credentials if mcp-reddit required them.
                # env=os.environ.copy()
            )
        )
        print(f"--- Successfully connected to mcp-reddit server. Discovered {len(tools)} tool(s). ---")
        # Print discovered tool names for debugging/instruction refinement
        for tool in tools:
            print(f"  - Discovered tool: {tool.name}") # Tool name is likely 'fetch_reddit_hot_threads' or similar
        return tools, exit_stack
    except FileNotFoundError:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: 'uvx' command not found. Please install uvx: pip install uvx !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Return empty tools and a no-op exit stack to prevent agent failure
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
        return [], DummyExitStack()
    except Exception as e:
        print(f"--- ERROR connecting to or starting mcp-reddit server: {e} ---")
        # Return empty tools and a no-op exit stack
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
        return [], DummyExitStack()


async def create_agent():
    """Creates the TTS speaker agent by connecting to the ElevenLabs MCP server via uvx."""
    tools, exit_stack = await get_tools_async()
    if not tools:
        print("--- WARNING: No tools discovered from MCP server. Agent will lack Reddit functionality. ---")

    # Define LLM for wrapping the tool output if needed
    llm = LiteLlm(model="gemini/gemini-1.5-flash-latest", api_key=os.environ.get("GOOGLE_API_KEY"))


    agent_instance = Agent(
        name="tts_speaker_agent",
        description="Converts provided text into speech using ElevenLabs TTS.",
        instruction=(
            "You are a Text-to-Speech agent. Convert user text to speech audio files.\n\n"
            "IMPORTANT FORMATTING RULES:\n"
            "1. Always call the text_to_speech tool with voice_name='Will'\n"
            "2. When the tool returns a file path, format your response like this example:\n"
            "   'I've converted your text to speech. The audio file is saved at `/path/to/file.mp3`'\n"
            "3. Make sure to put ONLY the file path inside backticks (`), not any additional text\n"
            "4. Never modify or abbreviate the path\n\n"
            "This exact format is critical for proper processing."
        ),
        model=llm,
        tools=tools,
    )

    return agent_instance, exit_stack

root_agent = create_agent()