# agent.py

import asyncio
import yaml
from core.loop import AgentLoop
from core.session import MultiMCP
from core.context import MemoryItem, AgentContext
import datetime
from pathlib import Path
import json
import re
from modules.history_manager import initialize_history_manager
from modules.memory import load_conversation_history, search_historical_conversations, add_conversation_to_history


def log(stage: str, msg: str):
    """Simple timestamped console logger."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}")

async def main():
    print("🧠 Cortex-R Agent Ready")
    current_session = None

    with open(r"/home/shiv-nlp-mldl-cv/Documents/EAGCode/Session9-Hybrid_Planning_for_Decision_Making/S9/config/profiles.yaml", "r") as f:
        profile = yaml.safe_load(f)
        mcp_servers_list = profile.get("mcp_servers", [])
        mcp_servers = {server["id"]: server for server in mcp_servers_list}

    multi_mcp = MultiMCP(server_configs=list(mcp_servers.values()))
    await multi_mcp.initialize()
    
    # Check history for similar queries
    history = load_conversation_history()
    # Initialize the history manager with the MCP dispatcher
    history_manager = initialize_history_manager(multi_mcp)
    log("agent", "🔍 Conversation history indexing enabled")

    try:
        
        while True:
            user_input = input("🧑 What do you want to solve today? → ")
            
            if user_input.lower() == 'exit':
                break
            if user_input.lower() == 'new':
                current_session = None
                continue

            while True:
                context = AgentContext(
                    user_input=user_input,
                    session_id=current_session,
                    dispatcher=multi_mcp,
                    mcp_server_descriptions=mcp_servers,
                )
                agent = AgentLoop(context)
                if not current_session:
                    current_session = context.session_id

                result = await agent.run()

                if isinstance(result, dict):
                    answer = result["result"]
                    if "FINAL_ANSWER:" in answer:
                        print(f"\n💡 Final Answer: {answer.split('FINAL_ANSWER:')[1].strip()}")   
                        add_conversation_to_history(user_input, answer.split('FINAL_ANSWER:')[1].strip(), history)                      
                        break
                    elif "FURTHER_PROCESSING_REQUIRED:" in answer:
                        user_input = answer.split("FURTHER_PROCESSING_REQUIRED:")[1].strip()
                        print(f"\n🔁 Further Processing Required: {user_input}")
                        continue  # 🧠 Re-run agent with updated input
                    else:
                        print(f"\n💡 Final Answer (raw): {answer}")
                        add_conversation_to_history(user_input, answer, history)     
                        break
                else:
                    print(f"\n💡 Final Answer (unexpected): {result}")
                    add_conversation_to_history(user_input, answer, history)     
                    break
    except KeyboardInterrupt:
        print("\n👋 Received exit signal. Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())


# Working
# Find the ASCII values of characters in INDIA and then return sum of exponentials of those values.
# How much Anmol singh paid for his DLF apartment via Capbridge? 

# After fix
# What is the log value of the amount that Anmol singh paid for his DLF apartment via Capbridge? 
# What do you know about Don Tapscott and Anthony Williams?
# What is the relationship between Gensol and Go-Auto?
# Summarize this page: https://theschoolof.ai/

# New questions
# What is the square root of the sum of the squares of 10, 20, and 30?
# Summarize this article for me https://surpriselib.com/
# What is the main theme of the book Atomic Habits? Hint: Use websearch
# What long-term vision did Elon Musk have for Tesla?  Hint: Use documentsearch
# What legal or business conflict was Tesla Motors involved in during 2013 in 500 words? Use documentsearch 