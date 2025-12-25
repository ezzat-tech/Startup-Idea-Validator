import logfire
from pydantic import BaseModel

logfire.configure(project_name='ezzat-tech/starter-project')
logfire.instrument_pydantic()

import streamlit as st
import asyncio
from agent import run_orchestrated_research
from models import VentureReport

# --- Page Config ---
st.set_page_config(
    page_title="AI Market Researcher",
    page_icon="🚀",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("🚀 AI Market Researcher")
st.markdown("Enter your startup idea below, and our AI scout will validate the market for you.")


# --- User Input ---
startup_input = st.text_area(
    "What's your startup idea?",
    placeholder="e.g., A high-end coffee subscription for offices in London...",
    height=100
)

# --- Execution ---
if st.button("Run Research Report"):
    if not startup_input:
        st.warning("Please enter a startup idea first!")
    else:
        with st.spinner("🔍 Scouting the market, analyzing competitors, and finding gaps..."):
            try:
                # Run the orchestrated multi-agent workflow
                async def run_research():
                    return await run_orchestrated_research(startup_input)

                report = asyncio.run(run_research())

                # --- Display Results ---
                st.success("✅ Research Complete!")
                st.divider()

                st.header(f"📊 Venture Report: {report.startup_name}")
                
                # Summary
                st.subheader("High-Level Summary")
                st.write(report.summary)

                # Competitors
                st.subheader("🏆 Key Competitors")
                for comp in report.competitors:
                    with st.expander(f"{comp.name}"):
                        st.write(f"**Description:** {comp.description}")
                        st.write(f"**Pricing:** {comp.pricing}")
                        st.write("**Strengths:**")
                        for s in comp.strengths:
                            st.markdown(f"- {s}")
                        st.write("**Weaknesses:**")
                        for w in comp.weaknesses:
                            st.markdown(f"- {w}")

                # Market Gaps
                st.subheader("💡 Identified Market Gaps")
                for gap in report.market_gaps:
                    st.markdown(f"### {gap.title}")
                    st.write(gap.description)
                    st.info(f"**Evidence:** {gap.evidence}")

                # Final Recommendation
                st.subheader("🏁 Final Recommendation")
                st.markdown(f"> {report.final_recommendation}")
                
                # Export JSON Option
                with st.expander("View Raw JSON Data"):
                    st.json(report.model_dump())

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Check your API keys in the .env file.")

# --- Footer ---
st.divider()
st.caption("AI Market Researcher v1.0 | Data powered by Perplexity AI")
