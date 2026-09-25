/*
  useChatSocket.js — Custom hook that manages the WebSocket connection.

  Responsibilities:
    - Open / close the WebSocket connection
    - Send user messages to the backend
    - Receive responses and update state
    - Track connection status (connecting / open / closed / error)

  *** CHANGE THE URL HERE if your backend runs on a different port ***
*/
import { useState, useEffect, useRef, useCallback } from "react";

// ── Single place to change the backend address ────────────────────────────────
const WS_URL = "ws://localhost:8000/ws/chat";

// Check if running on localhost / 127.0.0.1
const checkIsLocal = () =>
  typeof window !== "undefined" &&
  (window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1");

// Pre-scripted demo messages for deployed / visitor preview mode
const DEMO_MESSAGES = [
  {
    role: "user",
    text: "Find my Operating Systems lecture notes and check when Assignment 3 is due.",
  },
  {
    role: "bot",
    text: "I searched your notes and calendar:\n\n1. **Notes Found:** 'OS_Lecture_7_VirtualMemory.pdf'\n2. **Upcoming Deadline:** Assignment 3 (Memory Management) is due on **Friday, Oct 24 at 11:59 PM**.\n\nWould you like me to summarize Lecture 7 for you?",
  },
];

const DEMO_TOOL_TRACE = [
  {
    tool_name: "search_notes",
    input_args: { query: "Operating Systems" },
    result: { count: 1, file: "OS_Lecture_7_VirtualMemory.pdf" },
  },
  {
    tool_name: "get_calendar_events",
    input_args: { filter: "Assignment 3" },
    result: { title: "Assignment 3", due: "2026-10-24T23:59:00" },
  },
];

export function useChatSocket() {
  const isLocal = checkIsLocal();

  // List of chat messages: { role: "user"|"bot", text: string }
  const [messages, setMessages] = useState(isLocal ? [] : DEMO_MESSAGES);

  // Tool calls from the most recent bot turn: [{ tool_name, input_args, result }]
  const [toolTrace, setToolTrace] = useState(isLocal ? [] : DEMO_TOOL_TRACE);

  // "connecting" | "open" | "closed" | "error" | "demo"
  const [status, setStatus] = useState(isLocal ? "connecting" : "demo");

  // Are we waiting for a bot reply right now?
  const [isLoading, setIsLoading] = useState(false);

  // useRef keeps a stable reference to the WebSocket across re-renders
  const wsRef = useRef(null);

  // ── Open the WebSocket when the hook first mounts ─────────────────────────
  useEffect(() => {
    // If not on localhost, do NOT attempt WebSocket connection (Demo Preview mode)
    if (!isLocal) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("[useChatSocket] Connected to", WS_URL);
      setStatus("open");
    };

    ws.onmessage = (event) => {
      // Backend sends JSON: { answer, tool_trace } OR { error }
      const data = JSON.parse(event.data);

      if (data.error) {
        // Show the error as a bot message so the user sees it
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: `Error: ${data.error}` },
        ]);
      } else {
        // Normal response: add bot message and update tool trace
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: data.answer },
        ]);
        setToolTrace(data.tool_trace || []);
      }

      setIsLoading(false);  // bot has replied, stop showing spinner
    };

    ws.onerror = (err) => {
      console.error("[useChatSocket] WebSocket error:", err);
      setStatus("error");
      setIsLoading(false);
    };

    ws.onclose = () => {
      console.log("[useChatSocket] Disconnected.");
      setStatus("closed");
      setIsLoading(false);
    };

    // Cleanup: close the socket if the component unmounts
    return () => {
      ws.close();
    };
  }, [isLocal]); // empty or [isLocal] deps → runs on mount

  // ── sendMessage: called by InputBar when user hits Send ───────────────────
  const sendMessage = useCallback((text) => {
    if (!text.trim()) return;
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.warn("[useChatSocket] Socket not open, can't send.");
      return;
    }

    // Optimistically add the user message to the chat immediately
    setMessages((prev) => [...prev, { role: "user", text }]);

    // Clear the previous tool trace while we wait for the new one
    setToolTrace([]);
    setIsLoading(true);

    // Send to backend as JSON
    wsRef.current.send(JSON.stringify({ message: text }));
  }, []);

  return { messages, toolTrace, status, isLoading, sendMessage };
}
