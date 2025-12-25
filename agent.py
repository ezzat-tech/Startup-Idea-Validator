import logfire
from pydantic_ai import Agent, RunContext
from models import VentureReport
from tools import search_perplexity, crawl_website
import os
import asyncio

# Define the Agent FIRST
research_agent = Agent(
    'openai:gpt-4o',
    output_type=VentureReport,
    system_prompt=(
        "You are an expert Startup Scout and Market Analyst. "
        "Your goal is to validate startup ideas by researching the web. "
        "Be critical, find real data, and identify specific gaps in the market."
    )
)

# Now define the tools using the agent with logfire spans for readability
@research_agent.tool
def search_tool(ctx: RunContext, query: str) -> str:
    with logfire.span("🔎 Perplexity Search: {query}", query=query):
        return search_perplexity(query)

@research_agent.tool
def crawl_tool(ctx: RunContext, url: str) -> str:
    with logfire.span("🌐 Crawling Website: {url}", url=url):
        return crawl_website(url)

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