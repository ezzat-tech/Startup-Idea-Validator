import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API keys from .Env
load_dotenv()

# Initialize the Perplexity Client
# Remember: We use the standard OpenAI library for Perplexity!
client = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

def search_perplexity(query: str) -> str:
    """
    Searches the web using Perplexity AI to get real-time market data, competitors, and user pain points.
    """

    response = client.chat.completions.create(
        model="sonar",
        messages=[
            {
                "role": "system",
                "content": "You are a market research assistant. Provide consice, factual data with citations."

            },
            
            {
                "role": "user", "content": query
                
            }
        ]
    )
    return response.choices[0].message.content

import httpx # we will use this to fetch the website content

def crawl_website(url: str) -> str:
    """
    Crawls a specific URL to extract deeper information when Perplexity finds a relevant source.
    """
    try:
        # we use a simple 'r.text' approach for now to get the HTML/Text
        with httpx.Client() as client:
            response = client.get(url, timeout=10.0)
            # we take the first 4000 characters to avoid overwhelming the LLM
            return response.text[:4000]
    except Exception as e:
        return f"Error crawling {url}: {str(e)}"
    
