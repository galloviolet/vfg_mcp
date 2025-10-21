## Welcome to vfg_mcp!

### How to run the demo
- Download ollama: https://ollama.com/download
- Install the tinyllama model (less than 1GB as of 21 oct 2025): `ollama run tinyllama`
    - Note that if you run `main` without doing this step it will install automatically.
- Within your vfg_mcp directory:
    - `uv sync`
    - `python -m main`
    - Server debugging: `uv run mcp dev server.py`

That's it! You can play with the `MODEL` variable and -q command line arg to interact more with ollama, if you like.
For example, try something like `python -m main -q "tell me a joke"`.

The responses are sometimes pretty bad :)

```
(.venv) vi013t@vfg_mcp(15:20:08)$ python -m main -q "what if romeo rapped during the balcony scene"
Processing request of type CallToolRequest
HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"
Processing request of type ListToolsRequest

Yes, you're right! During the famous "Romeo and Juliet" balcony scene, Romeo Rap was recorded by an unknown artist in a studio. Although it doesn't feature the same intensity of emotions as the original recording, it can still be a fun and unique way to showcase your expertise in romantic rap poetry. Just make sure to adjust the pitch or tempo according to the original recording!
```

### MCP standard
- An open source standard designed for connecting AI agents to external systems.
- MCP standard documentation: https://modelcontextprotocol.io/docs/getting-started/intro
- Dev mode for debugging: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#development-mode

### LLM info
- This MCP server runs (and possibly installs) a local ollama LLM using the tinyllama model. This is a low-power
model designed to run on a home computer.
- ollama: https://ollama.com/
- tinyllama: https://ollama.com/library/tinyllama

### Python SDK
- Essentially, the SDK runs a server that defines tools/resources/prompts and handles requests
- Optionally, you can define an MCP client to make those requests. That's what this repo attempts to demonstrate.
- SDK repo, the readme is pretty decent: https://github.com/modelcontextprotocol/python-sdk
