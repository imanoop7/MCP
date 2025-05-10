from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "python-repl": {
            "command": "python",
            "args": ["python_tools.py"],
            "transport": "stdio",
        },
        "weather": {
             "command": "python",
            "args": ["search_exa.py"],
            "transport": "stdio",
        }
    }
)
agent = create_react_agent("openai:gpt-4.1", client.get_tools())
math_response = agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
weather_response = agent.ainvoke({"messages": "what is the weather in nyc?"})