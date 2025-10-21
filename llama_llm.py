from subprocess import Popen

from ollama import ChatResponse, chat

MODEL = "tinyllama"


class LlamaLLM:
    """Simple example of a local LLM model."""
    def __init__(self):
        self.proc: Popen | None = None

    async def start(self) -> None:
        """Connect to database."""
        self.proc = Popen(["ollama", "run", MODEL])
        print("Connected to LLM")

    async def stop(self) -> None:
        """Disconnect from database."""
        self.proc.terminate()
        print("Stopping LLM")

    def ask(self, prompt: str, role: str = "user") -> str:
        """Ask the LLM a question and return the response."""
        chat_response: ChatResponse = chat(
            model=MODEL, messages=[{"role": role, "content": prompt}]
            )
        return chat_response["message"]["content"]
