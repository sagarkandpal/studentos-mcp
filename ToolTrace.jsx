/*
  ToolTrace.jsx — Side panel showing which MCP tools were called
                  during the most recent bot turn.

  Props:
    toolTrace: array of { tool_name, input_args, result }
               (empty array when no tools were called, or between turns)

  Each entry shows:
    - Tool name  (e.g. "search_notes")
    - Input args (what was passed in)
    - Result     (what the tool returned)
*/
import React from "react";

export default function ToolTrace({ toolTrace }) {
  const panelStyle = {
    width: "320px",
    minWidth: "320px",
    borderLeft: "1px solid #374151",
    backgroundColor: "#111827",
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
    padding: "16px",
  };

  const headingStyle = {
    fontSize: "12px",
    fontWeight: "700",
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "#6b7280",
    marginBottom: "12px",
  };

  const emptyStyle = {
    fontSize: "13px",
    color: "#4b5563",
    fontStyle: "italic",
  };

  const cardStyle = {
    backgroundColor: "#1f2937",
    borderRadius: "8px",
    padding: "12px",
    marginBottom: "10px",
    fontSize: "13px",
  };

  const toolNameStyle = {
    fontWeight: "700",
    color: "#60a5fa",   // blue
    marginBottom: "6px",
  };

  const labelStyle = {
    fontSize: "11px",
    fontWeight: "600",
    color: "#9ca3af",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginTop: "8px",
    marginBottom: "2px",
  };

  const codeStyle = {
    backgroundColor: "#111827",
    borderRadius: "4px",
    padding: "6px 8px",
    fontSize: "12px",
    color: "#d1d5db",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    maxHeight: "100px",
    overflowY: "auto",
  };

  return (
    <div style={panelStyle}>
      <p style={headingStyle}>🔧 Tool Trace</p>

      {toolTrace.length === 0 ? (
        <p style={emptyStyle}>No tools called yet.</p>
      ) : (
        toolTrace.map((entry, idx) => (
          <div key={idx} style={cardStyle}>
            {/* Tool name */}
            <div style={toolNameStyle}>{entry.tool_name}</div>

            {/* Input args */}
            <div style={labelStyle}>Input</div>
            <pre style={codeStyle}>
              {JSON.stringify(entry.input_args, null, 2)}
            </pre>

            {/* Result */}
            <div style={labelStyle}>Result</div>
            <pre style={codeStyle}>
              {entry.result ?? "(no result)"}
            </pre>
          </div>
        ))
      )}
    </div>
  );
}
