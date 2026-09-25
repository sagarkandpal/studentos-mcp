/*
  ChatWindow.jsx — Scrollable list of all chat messages.

  Props:
    messages:  array of { role, text } objects from useChatSocket
    isLoading: boolean — true while waiting for a bot reply

  - Renders a MessageBubble for each message.
  - Shows a "Thinking…" indicator at the bottom when isLoading is true.
  - Auto-scrolls to the latest message.
*/
import React, { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, isLoading }) {
  // We'll attach this ref to a dummy div at the bottom of the list
  // and scroll to it whenever messages change.
  const bottomRef = useRef(null);

  useEffect(() => {
    // Every time a new message appears, scroll down
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const containerStyle = {
    flex: 1,                  // take all available vertical space
    overflowY: "auto",        // scroll when content overflows
    padding: "16px",
    display: "flex",
    flexDirection: "column",
  };

  const emptyStyle = {
    margin: "auto",
    color: "#6b7280",
    fontSize: "14px",
    textAlign: "center",
  };

  const thinkingStyle = {
    display: "flex",
    justifyContent: "flex-start",
    marginBottom: "12px",
  };

  const thinkingBubbleStyle = {
    padding: "10px 14px",
    borderRadius: "18px 18px 18px 4px",
    backgroundColor: "#374151",
    color: "#9ca3af",
    fontSize: "14px",
    fontStyle: "italic",
  };

  return (
    <div style={containerStyle}>
      {/* Show hint text when chat is empty */}
      {messages.length === 0 && !isLoading && (
        <p style={emptyStyle}>Ask StudentOS anything to get started 👋</p>
      )}

      {/* One bubble per message */}
      {messages.map((msg, idx) => (
        <MessageBubble key={idx} message={msg} />
      ))}

      {/* Thinking indicator while waiting for the bot */}
      {isLoading && (
        <div style={thinkingStyle}>
          <div style={thinkingBubbleStyle}>Thinking…</div>
        </div>
      )}

      {/* Invisible anchor — we scroll to this */}
      <div ref={bottomRef} />
    </div>
  );
}
