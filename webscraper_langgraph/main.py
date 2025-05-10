import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

# Example query
# "What is weather in newyork"
# "What is FastMCP?"
# "summarize this youtube video in 50 words, here is a video link: https://www.youtube.com/watch?v=2f3K43FHRKo"
query = input("Query:")

# Define llm
model = ChatOllama(model="llama3.2")

# Define MCP servers
async def run_agent():
    async with MultiServerMCPClient(
        {
            "python-repl": {
                "command": "python",
                "args": ["python_tools.py"],
                "transport": "stdio",
            },
            "search": {
                "command": "python",
                "args": ["search_exa.py"],
                "transport": "stdio",
            }, 
        }
    ) as client:
        # Load available tools
        tools = client.get_tools()
        agent = create_react_agent(model, tools)

        # Add system message
        system_message = SystemMessage(content=(
                "You have access to multiple tools that can help answer queries. "
                "Use them dynamically and efficiently based on the user's request. "
        ))

        # Process the query
        agent_response = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})

        # # Print each message for debugging
        # for m in agent_response["messages"]:
        #     m.pretty_print()

        return agent_response["messages"][-1].content

# Run the agent
if __name__ == "__main__":
    response = asyncio.run(run_agent())
    print("\nFinal Response:", response)