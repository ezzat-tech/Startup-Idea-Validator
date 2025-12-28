import logfire
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Configure Logfire
logfire.configure(project_name='ezzat-tech/starter-project')
logfire.instrument_pydantic()

from agent import run_orchestrated_research
from models import VentureReport

# Create the FastAPI app
app = FastAPI(
    title="Startup Idea Validator API",
    description="Validate startup ideas with AI-powered market research",
    version="1.0.0"
)

# Request model - what the user sends
class ResearchRequest(BaseModel):
    startup_idea: str = Field(..., description="The description of your startup idea (eg., 'AI powered coffee subscription')")

# Response model - what we send back
class ResearchResponse(BaseModel):
    success: bool
    report: VentureReport | None = None
    error: str | None = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Startup Idea Validator API!"}

@app.post("/research", response_model=ResearchResponse)
async def research_startup(request: ResearchRequest):
    """
    Submit a startup idea and receive a detailed market research report.
    """
    try:
        with logfire.span("🌐 API Request: {idea}", idea=request.startup_idea[:50]):
            report = await run_orchestrated_research(request.startup_idea)
            return ResearchResponse(success=True, report=report)
    except Exception as e:
        return ResearchResponse(success=False, error=str(e))