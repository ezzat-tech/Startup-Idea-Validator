import logfire
from pydantic_ai import Agent, RunContext
from models import VentureReport, Critique
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

# The Critic Agent - Its only job is to find flaws
critic_agent = Agent(
    'openai:gpt-4o-mini',  # We use a cheaper model for criticism
    output_type=Critique,
    system_prompt=(
        "You are a harsh but fair Quality Analyst for startup research reports. "
        "Your job is to find weaknesses in the report. "
        "Check if competitors have complete pricing and weakness data. "
        "Check if market gaps have real evidence, not just opinions. "
        "Be specific in your feedback so the Researcher can fix it."
    )
)

async def run_orchestrated_research(user_prompt: str) -> VentureReport:
    """
    Orchestrates a multi-agent research workflow:
    1. Researcher creates initial report
    2. Critic audits the report
    3. If issues found, Researcher refines it
    """
    with logfire.span("🧠 Orchestrated Research Pipeline"):
        
        # Stage 1: Initial Research
        with logfire.span("📊 Stage 1: Initial Research"):
            initial_result = await research_agent.run(user_prompt)
            initial_report = initial_result.output

        # Stage 2: Critique
        with logfire.span("🔍 Stage 2: Critic Review"):
            critique_prompt = f"""
            Please audit this startup research report for quality and completeness:
            
            Startup: {initial_report.startup_name}
            Summary: {initial_report.summary}
            Competitors: {[c.name for c in initial_report.competitors]}
            Market Gaps: {[g.title for g in initial_report.market_gaps]}
            
            Full Report JSON:
            {initial_report.model_dump_json(indent=2)}
            """
            critique_result = await critic_agent.run(critique_prompt)
            critique = critique_result.output

        # Stage 3: Refinement (if needed)
        if critique.has_issues:
            with logfire.span("🔧 Stage 3: Refinement"):
                refinement_prompt = f"""
                Original research topic: {user_prompt}
                
                The Quality Analyst found these issues with your previous report:
                - Missing competitor info: {critique.missing_competitor_info}
                - Vague market gaps: {critique.vague_market_gaps}
                - Feedback: {critique.actionable_feedback}
                
                Please conduct additional research to fix these specific issues 
                and produce an improved, complete VentureReport.
                """
                refined_result = await research_agent.run(refinement_prompt)
                return refined_result.output
        
        # No issues found, return the original
        return initial_report

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