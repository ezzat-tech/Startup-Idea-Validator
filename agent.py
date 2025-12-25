from pydantic_ai import Agent, RunContext
from models import VentureReport
from tools import search_perplexity, crawl_website
import os

# Define the Agent
# We tell it:
# 1. Which model to use
# 2. What the output should be

research_agent = Agent(
    'openai:gpt-4o',
    output_type=VentureReport,
    system_prompt=(
        "You are an expert Startup Scout and Market Analyst. "
        "Your goal is to validate startup ideas by researching the web. "
        "Be critical, find real data, and identify specific gaps in the market."
    )
)

@research_agent.tool
def search_tool(ctx: RunContext, query: str) -> str:
    return search_perplexity(query)

@research_agent.tool
def crawl_tool(ctx: RunContext, url: str) -> str:
    """Crawl a specific website for more detail."""
    return crawl_website(url)

import asyncio

async def main():
    # Define a sample Lookup
    prompt = "A high-end, AI-powered specialized coffee subscription for office spaces in London."

    print(f'🚀 Researching: {prompt}...')

    # Run the agent
    result = await research_agent.run(prompt)

    # Print the structured output
    print("\n--- Venture Report ---")
    print(result.output.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())

    