# 🌟 Cortex-R: Hybrid Planning Agent System 🌟

Cortex-R is a memory-augmented, perception-aware, and tool-using AI agent. It combines LLM planning, sandboxed code execution, and tool orchestration through dynamic MCP servers.

📎 Related Reports:📝 QA Report|📊 Prompt Comparison Report

[📝 QA Report](QA_report.md)

[📊 Prompt Comparison Report](Prompt_Comparsion_Report.md)

## 🧱 File Structure

- core/ – Controls the loop, context, session, and strategy modules.
- modules/ – Houses perception, decision, heuristics, and memory logic.
- mcp_servers/ – Distributed servers for executing math, search, RAG, etc.
- config/ – Stores model and server profiles in JSON/YAML format.
- agent.py – Main CLI entry that initiates the entire lifecycle.

## 🧠 Architecture

Step 1: User query is processed through the perception layer to extract tool hints.
Step 2: Planning module creates a solve() plan using prompt templates and strategy.

Step 3: Action layer executes the plan in a sandbox with retry logic.
Step 4: Memory logs results, and historical context can affect future plans.

## ✨ Features

- Hybrid Planning: Uses both exploratory and conservative approaches to tool use.
- Dynamic Tool Selection: Filters and calls tools based on intent and memory success.
- Sandboxed Execution: All plans are run safely with controlled tool access.
- Contextual Memory: Remembers past questions, answers, and tool effectiveness.
- RAG & Websearch: Integrates document and web search as first-class tools.

## 🛡️ Heuristics Engine

- Validates Inputs: Checks for length, NSFW content, and malformed URLs/emails.
- Sanitizes Outputs: Auto-fixes common JSON issues and missing required fields.

## 🔧 MCP Tool Servers

- mcp_server_1: Offers math operations, string tools, factorial, and log tools.
- mcp_server_2: Provides PDF/webpage extraction and FAISS-based RAG search.
- mcp_server_3: Powers DuckDuckGo search and raw HTML extraction tools.
- mcp_memory: Enables historical search, session indexing, and recall insights.

## 📚 Memory & Recall

- Tool Logs: Records every tool used, inputs, results, and success status.
- History Lookup: Retrieves related queries and outputs from past sessions.

## 📥 Sample Questions

- 🔢 What is the square root of the sum of the squares of 10, 20, and 30?
- 📰 Summarize this article for me https://surpriselib.com/
- 📘 What is the main theme of the book Atomic Habits? Hint: Use websearch
- 🚗 What long-term vision did Elon Musk have for Tesla? Hint: Use documentsearch
- ⚖️ What legal or business conflict was Tesla Motors involved in during 2013 in 500 words? Use documentsearch

## 🔁 Enhanced Workflow Summary

- Memory Lookup: Looks for similar past answers before tool invocation.
- Perception First: Identifies query type, relevant tools, and intent.
- Smarter Planning: Generates solve() with dynamic prompt logic.
- Sandboxed Run: Executes and evaluates tool output safely.
- Memory Write-back: Saves answers for future context reuse.