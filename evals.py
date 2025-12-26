import asyncio
import logfire
from pydantic_ai import Agent
from models import VentureReport, EvalResult
from agent import run_orchestrated_research

# Configure logfire for evals
logfire.configure(project_name="ezzat-tech/starter-project")

# --- Test Cases ---
# These are the startup ideas we'll use to test the agent
TEST_CASES = [
    "An AI-powered resume builder for recent college graduates",
    "A subscription box for exotic pet owners",
    "A mobile app that connects local farmers directly with restaurants"
]


# --- The Judge Agent ---
judge_agent = Agent(
    model="openai:gpt-4o-mini",
    output_type=EvalResult,
    system_prompt=
    "You are a strict Quality Evaluator for startup market research reports. " 
    "Grade the report on a scale of 1-10 for each criterion. " 
    "Be harsh but fair. A score of 7+ means the report is production-ready. " 
    "A score below 5 means there are serious issues. " 
    "Always explain your reasoning."
    
)

async def evaluate_report(report: VentureReport) -> EvalResult:
    """Ask the judge to grade a single report"""
    with logfire.span("Judging report: {name}", name=report.startup_name):
        judge_prompt = f"""
        Please evaluate this startup research report:

        Startup Name: {report.startup_name}
        Summary: {report.summary}
        
        Competitors Found: {len(report.competitors)}
        {chr(10).join([f"- {c.name}: Pricing={c.pricing}, Strengths={len(c.strengths)}, Weaknesses={len(c.weaknesses)}" for c in report.competitors])}

        Market Gaps Found: {len(report.market_gaps)}
        {chr(10).join([f"- {g.title}: Evidence={g.evidence[:100]}..."for g in report.market_gaps])}
    
        Final Recommendation: {report.final_recommendation}
        """
        result = await judge_agent.run(judge_prompt)
        return result.output

async def run_eval_suite():
    """Run the full evaluation suite."""
    print("=" * 60)
    print("STARTING EVALUATION SUITE")
    print("=" * 60)

    result = []

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n Test Case {i}/{len(TEST_CASES)}: {test_case[:50]}...")

        # Run the orchestrated research
        report = await run_orchestrated_research(test_case)

        # Grade the report
        eval_result = await evaluate_report(report)
        result.append(eval_result)

        # Print individual Scores
        print(f"   📊 Competitor Quality: {eval_result.competitors_quality_score}/10")
        print(f"   📊 Market Gap Quality: {eval_result.market_gaps_quality_score}/10")
        print(f"   📊 Evidence Score: {eval_result.evidence_score}/10")
        print(f"   ⭐ Overall Score: {eval_result.overall_score}/10")
        print(f"   💬 Reasoning: {eval_result.reasoning[:100]}...")

    # Calculate averages
    avg_overall = sum(r.overall_score for r in result) / len(result)
    avg_competitor = sum(r.competitors_quality_score for r in result) / len(result)
    avg_gaps = sum(r.market_gaps_quality_score for r in result) / len(result)
    avg_evidence = sum(r.evidence_score for r in result) / len(result)

    print("\n" + "=" * 60)
    print("📈 FINAL EVALUATION SUMMARY")
    print("=" * 60)
    print(f"   Average Competitor Quality: {avg_competitor:.1f}/10")
    print(f"   Average Market Gap Quality: {avg_gaps:.1f}/10")
    print(f"   Average Evidence Score: {avg_evidence:.1f}/10")
    print(f"   🏆 OVERALL AVERAGE: {avg_overall:.1f}/10")

    if avg_overall >= 7:
        print("\n 🎉 Your agent is PRODUCTION READY!")
    elif avg_overall >= 5:
        print("\n 🚨 Your agent needs improvement. Review the weak areas.")
    else:
        print("\n ⚠️ Your agent has serious issues. Debug before deploying.")

if __name__ == "__main__":
    asyncio.run(run_eval_suite())

  



