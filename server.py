from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from os import getcwd

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from llama_llm import LlamaLLM


@dataclass
class AppContext:
    """Application context with typed dependencies."""
    llm: LlamaLLM

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type safety."""
    assert server
    llm = LlamaLLM()
    await llm.start()
    try:
        yield AppContext(llm=llm)
    finally:
        await llm.stop()


# pass lifespan to server
mcp = FastMCP("vfg_llm", lifespan=app_lifespan)


# access type safe lifespan context in tools
@mcp.tool()
def ask_llm(ctx: Context[ServerSession, AppContext], question: str) -> str:
    """Ask the LLM a question and get the response."""
    assert ctx
    llm = mcp.get_context().request_context.lifespan_context.llm
    return llm.ask(prompt=question)


@mcp.tool()
def addition(a: int, b:int) -> int:
    """Example of a tool as a Python function."""
    return a + b

cwd = getcwd()
@mcp.resource(f"file://{cwd}/docs/" + "{name}")
def read_document(name: str | None) -> str:
    """Returns the contents of the requested document."""
    try:
        with open(f"{cwd}/docs/{name}", "r", encoding="UTF-8") as f:
            return f.read()
    except OSError as e:
        return getattr(e, "msg", "Failed to open file")



@mcp.resource("config://settings")
def get_settings() -> str:
    """Mocks an endpoint to return user settings."""
    return "{'theme': 'dark', 'language': 'en', 'debug': false}"


@mcp.prompt()
def greet_user(name: str, style: str = "hello") -> str:
    """Example of a prompt to provide to the LLM."""
    styles = {
        "hello": f"say hello to {name} in one sentence",
        "goodbye": f"say goodbye to {name} in one sentence",
    }
    return f"{styles.get(style, styles['hello'])}"


def main():
    """Entry point for direct execution server."""
    mcp.run()


if __name__ == "__main__":
    main()
