# AI Market Researcher

A professional market research application that validates startup ideas by conducting real-time web research and providing structured analytical reports.

The application leverages the power of Pydantic AI for agentic orchestration, Perplexity AI for real-time web searching, and Streamlit for the user interface.

## Overview

The AI Market Researcher acts as an expert Startup Scout and Market Analyst. It takes a startup idea as input, researches the current market landscape using live data, identifies competitors, and provides a structured venture report including market gaps and final recommendations.

## Core Features

- Real-time web research using Perplexity AI.
- Structured data extraction and validation with Pydantic and Pydantic AI.
- Detailed competitor analysis.
- Market gap identification based on search evidence.
- Final strategic recommendations for founders.
- Clean and intuitive web interface.

## Technology Stack

- **Python**: Core programming language.
- **Pydantic AI**: Agent framework and structured output enforcement.
- **Perplexity AI**: Real-time web search and reasoning API.
- **OpenAI**: Primary language model (GPT-4o).
- **Streamlit**: Web-based user interface.
- **Httpx**: For supplementary web crawling.

## Prerequisites

- Python 3.10 or higher.
- OpenAI API Key.
- Perplexity API Key.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory and add your API keys:

```text
OPENAI_API_KEY=your_openai_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
```

## Usage

To start the application, run the following command from the project root:

```bash
streamlit run app.py
```

Once the server starts, navigate to the URL provided in the terminal (usually `http://localhost:8501`) to begin your market research.