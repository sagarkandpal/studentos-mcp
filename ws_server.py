"""
ws_server.py — WebSocket bridge between the React frontend and the MCP agent.

This file does the SAME thing chatbot.py does, just swaps out
    input("You: ")   →  receive from WebSocket
    print("Bot:", …) →  send JSON back over WebSocket

That's literally the only difference.  All the MCP connection logic,
tool-loading, and agent setup are copy-pasted from chatbot.py and kept
identical so you can compare them side by side.
"""

import os
import asyncio
import json
import traceback

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from langchain_groq import ChatGroq
from langchain.agents import create_agent   # same import as chatbot.py

# ── Load .env (for GROQ_API_KEY) ────────────────────────────────────────────
load_dotenv()

# ── Path to the MCP server — same calculation as chatbot.py ──────────────────
# ws_server.py lives at  client/backend/ws_server.py
# server/main.py lives at  server/main.py
# So we go up two levels (backend → client → root) then into server/
SERVER_PATH = os.path.join(
    os.path.dirname(__file__),  # .../client/backend/
    "..",                        # .../client/
    "..",                        # .../  (project root)
    "server",
    "main.py",
)

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI()

# Allow the React dev-server (running on a different port) to connect.
# In production you would lock this down to your actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for local development
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helper: extract tool calls from LangChain agent result ────────────────────
def extract_tool_calls(messages: list) -> list:
    """
    Walk through all messages that came back from agent.ainvoke() and
    collect every tool-call/tool-result pair.

    LangChain gives us a list of messages like:
        HumanMessage        <- the user's question
        AIMessage           <- model decides to call a tool
          .tool_calls = [{"name": "search_notes", "args": {...}, "id": "..."}]
        ToolMessage         <- the tool's output
        AIMessage           <- final answer (no tool_calls)

    We zip AIMessage tool-calls with the ToolMessage that follows them.
    """
    tool_trace = []

    for i, msg in enumerate(messages):
        # AIMessage that contains at least one tool call
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                entry = {
                    "tool_name":  tc.get("name", "unknown"),
                    "input_args": tc.get("args", {}),
                    "result":     None,   # filled in below if we find it
                }

                # The very next message should be the ToolMessage for this call
                if i + 1 < len(messages):
                    next_msg = messages[i + 1]
                    # ToolMessage has a .content attribute with the result
                    if hasattr(next_msg, "content"):
                        entry["result"] = next_msg.content

                tool_trace.append(entry)

    return tool_trace


# ── The main WebSocket endpoint ────────────────────────────────────────────────
@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    """
    One WebSocket connection = one chat session.

    Setup (runs once when frontend connects):
      1. Start the MCP server subprocess (same as chatbot.py)
      2. Open a ClientSession and initialise it (same)
      3. Load tools via load_mcp_tools (same)
      4. Build the Gemini model (same)
      5. Create the agent (same)

    Then loop:
      - Wait for a JSON message from the frontend: {"message": "..."}
      - Run agent.ainvoke(...) exactly like chatbot.py does
      - Extract the final text answer + any tool calls that happened
      - Send back JSON: {"answer": "...", "tool_trace": [...]}
    """
    await websocket.accept()
    print("[ws_server] Client connected.")

    # ── Same server params as chatbot.py ──────────────────────────────────────
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_PATH],
    )

    try:
        # ── Same MCP connection + agent setup as chatbot.py ───────────────────
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await load_mcp_tools(session)
                print(f"[ws_server] Loaded {len(tools)} tools: {[t.name for t in tools]}")

                # Same LLM as chatbot.py
                model = ChatGroq(model="openai/gpt-oss-20b")

                # Same agent creation as chatbot.py
                agent = create_agent(model, tools)

                print("[ws_server] Agent ready. Waiting for messages...")

                # ── Message loop (replaces the while True: input() loop) ───────
                while True:
                    # Wait for the frontend to send a message
                    raw = await websocket.receive_text()

                    # Frontend sends JSON: { "message": "user's question" }
                    data = json.loads(raw)
                    user_input = data.get("message", "").strip()

                    if not user_input:
                        continue   # ignore empty messages

                    print(f"[ws_server] User: {user_input}")

                    # ── Same ainvoke call as chatbot.py ───────────────────────
                    result = await agent.ainvoke({
                        "messages": [
                            ("system",
                             "Answer directly and concisely. Do not offer numbered "
                             "menus of options, and do not ask follow-up questions "
                             "unless the request is genuinely ambiguous. If a tool "
                             "returns an error, state the exact error message plainly."),
                            ("user", user_input),
                        ]
                    })

                    # ── Same answer extraction as chatbot.py ──────────────────
                    final_message = result["messages"][-1]
                    content = final_message.content
                    if isinstance(content, list):
                        # Gemini can return a list of content blocks
                        answer_text = "".join(
                            block.get("text", "")
                            for block in content
                            if isinstance(block, dict)
                        )
                    else:
                        answer_text = content

                    print(f"[ws_server] Bot: {answer_text[:80]}...")

                    # ── NEW: collect tool calls so the UI can show them ────────
                    tool_trace = extract_tool_calls(result["messages"])

                    # ── Send result back to frontend ───────────────────────────
                    await websocket.send_text(json.dumps({
                        "answer":     answer_text,
                        "tool_trace": tool_trace,
                    }))

    except WebSocketDisconnect:
        # Client closed the tab / refreshed -- this is normal, not an error
        print("[ws_server] Client disconnected.")

    except Exception as e:
        # Something went wrong — tell the frontend and close cleanly
        print(f"[ws_server] Error: {e}")
        traceback.print_exc()
        try:
            await websocket.send_text(json.dumps({
                "error": str(e)
            }))
        except Exception:
            pass   # WebSocket might already be gone
