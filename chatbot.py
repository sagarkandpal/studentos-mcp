import asyncio
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()  # reads GROQ_API_KEY from .env

# path to our server's main.py (server is a sibling folder to client)
SERVER_PATH = os.path.join(os.path.dirname(__file__), "..", "server", "main.py")


async def main():
    # 1. Tell it how to start our server (as a subprocess, talking over stdio)
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_PATH],
    )

    # 2. Actually launch the server and open a session with it
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. Fetch the server's tools, already converted into LangChain tool objects
            tools = await load_mcp_tools(session)
            print(f"Connected. Server exposes {len(tools)} tools:", [t.name for t in tools])

            # 4. Our LLM (Groq)
            model = ChatGroq(model="openai/gpt-oss-20b")

            # 5. create_react_agent builds the ENTIRE loop for us:
            #    user message -> model decides if a tool is needed -> calls tool ->
            #    feeds result back to model -> model gives final answer.
            #    We don't have to write that loop by hand anymore.
            agent = create_agent(model, tools)

            print("\nStudentOS chatbot ready. Type 'exit' to quit.\n")

            while True:
                user_input = input("You: ")
                if user_input.strip().lower() == "exit":
                    break

                # 6. Send the message to the agent, get back the whole conversation
                result = await agent.ainvoke({
                    "messages": [
                        ("system", "Answer directly and concisely. Do not offer numbered "
                                "menus of options, and do not ask follow-up questions "
                                "unless the request is genuinely ambiguous. If a tool "
                                "returns an error, state the exact error message plainly."),
                        ("user", user_input),
                    ]
                })

                # 7. The last message in the list is the agent's final answer
                final_message = result["messages"][-1]
                content = final_message.content
                if isinstance(content, list):
                    # Gemini returns a list of blocks; pull out just the text parts
                    text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
                else:
                    text = content

                print("Bot:", text)


if __name__ == "__main__":
    asyncio.run(main())