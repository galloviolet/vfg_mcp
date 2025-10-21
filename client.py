from os import getcwd

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

from llama_llm import MODEL

server_params = StdioServerParameters(
    command="uv", args=["run", "python", "-m", "server", "stdio"], env=None
)

def handle_sampling_message(
        context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
    ) -> types.CreateMessageResult:
    """Sample handling, not used in example as-is."""
    assert context  # unused for now
    print(f"Sampling request: {params.messages}")
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! From, Model",
        ),
        model=MODEL,
        stopReason="endTurn",
    )


async def run():
    """Runs the client asynchronously, shows some examples of server calls"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            await session.initialize()

            prompts = await session.list_prompts()
            print(f"Available prompts: {[p.name for p in prompts.prompts]}")

            if prompts.prompts:
                prompt = await session.get_prompt(
                    "greet_user", arguments={"name": "Alice", "style": "hello"}
                )
                prompt = prompt.messages[0].content.text
            else:
                prompt = "scold the user for not asking a question"
            print(f"Prompt result: {prompt}")

            resources = await session.list_resources()
            print(f"Available resources: {[r.uri for r in resources.resources]}")

            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            cwd = getcwd()
            resource_content = await session.read_resource(f"file://{cwd}/docs/hello_world.txt")
            content_block = resource_content.contents[0]
            print(f"Resource content: {content_block.text}")

            response = await session.call_tool("ask_llm", arguments={"question": prompt})
            print(f"LLM response: {response.content[0].text}")


async def custom_run(question: str):
    """Ask the LLM a custom user-provided question."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            await session.initialize()

            response = await session.call_tool("ask_llm", arguments={"question": question})
            print(f"\n{response.content[0].text}")


async def demo():
    """Simple MCP demo."""
    run()

async def custom_question(question: str):
    """Ask a custom question."""
    custom_run(question)
