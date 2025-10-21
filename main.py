import argparse
import asyncio

import client


def main():
    """Run the example MCP client code that interacts with the server."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", help="Question to ask the LLM")
    args = parser.parse_args()
    if args.q is None:
        asyncio.run(client.run())
    else:
        asyncio.run(client.custom_run(args.q))

if __name__ == "__main__":
    main()
