# studentos-mcp

# 🎓 StudentOS MCP

> An AI-powered student assistant built with the Model Context Protocol (MCP) to bring GitHub, Google Drive, Calendar, deadlines, repositories, resumes, and student workflows together in one place.

StudentOS is an AI assistant designed to help students manage their academic and development workflow through natural language.

Instead of manually checking multiple platforms, students can interact with StudentOS and ask questions like:

- "Show me my GitHub repositories"
- "What are my upcoming deadlines?"
- "Find my recent commits"
- "Get my calendar events"
- "Find collaborators for my project"
- "Analyze my resume"
- "Create a tailored resume for this opportunity"

The assistant uses MCP tools to connect the AI with external services and student data.

---

## ✨ Features

### 🐙 GitHub Integration

StudentOS can interact with GitHub to help students understand and manage their development activity.

- Get GitHub repositories
- Get repository details
- Read repository README files
- Get file contents
- Analyze GitHub activity
- Fetch recent commits
- Find potential collaborators

### 📅 Calendar & Deadlines

Stay updated with important events and tasks.

- Fetch calendar events
- Identify upcoming deadlines
- Organize important student activities
- Ask questions about upcoming schedules

### 📄 Resume Intelligence

StudentOS can work with resumes and help students improve them.

- Import resume PDFs
- Extract resume information
- Analyze skills
- Track skills using student data
- Generate tailored resumes based on opportunities

### 🤖 AI Chat Interface

The project includes a custom chat interface with components such as:

- Chat Window
- Message Bubble
- Input Bar
- Tool Trace

This allows users to interact with the AI assistant while also seeing the tools being used behind the scenes.

---

## 🧠 Architecture

StudentOS follows an MCP-based architecture where the AI assistant can call specialized tools depending on the user's request.

```text
                    ┌─────────────────────┐
                    │      Student        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Chat Interface   │
                    │      (React UI)      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Chatbot       │
                    │      + MCP Client    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │  MCP Tools   │      │ Student Data │
             └──────┬───────┘      └──────────────┘
                    │
        ┌───────────┼───────────────┐
        ▼           ▼               ▼
     GitHub      Calendar       Google Drive
        │           │               │
        └───────────┼───────────────┘
                    │
                    ▼
             Resume / Student
                 Workflow
