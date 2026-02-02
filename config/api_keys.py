"""
API Keys Configuration
Copy this file and add your actual API keys
"""
import os
from typing import Optional

def get_api_key(service: str) -> Optional[str]:
    """Get API key for a specific service"""
    key_mapping = {
        "newsapi": "NEWSAPI_KEY",
        "guardian": "GUARDIAN_API_KEY", 
        "newsdata": "NEWSDATA_API_KEY"
    }
    
    env_var = key_mapping.get(service)
    if env_var:
        return os.getenv(env_var)
    return None

# API Keys - Replace with your actual keys or set as environment variables
API_KEYS = {
    # NewsAPI.org - Get free key at: https://newsapi.org/register
    "newsapi": get_api_key("newsapi") or "d6cabf87c31d4de1acf3442348228cce",
    
    # The Guardian API - Get free key at: https://bonobo.capi.gutools.co.uk/register/developer
    "guardian": get_api_key("guardian") or "cb8b4bf8-6fd5-42d6-bf65-ee02df92d6be",
    
    # NewsData.io - Get free key at: https://newsdata.io/register
    "newsdata": get_api_key("newsdata") or "pub_2ef38e6f49384427869f4be7ea315b15"
}

# Validation
def validate_api_keys() -> dict:
    """Validate that API keys are configured"""
    status = {}
    for service, key in API_KEYS.items():
        if key and key != f"your_{service}_api_key_here":
            status[service] = "configured"
        else:
            status[service] = "missing"
    return status

# Instructions for getting API keys
API_INSTRUCTIONS = {
    "newsapi": {
        "url": "https://newsapi.org/register",
        "steps": [
            "1. Go to https://newsapi.org/register",
            "2. Sign up with your email",
            "3. Verify your email address", 
            "4. Copy your API key from the dashboard",
            "5. Set NEWSAPI_KEY environment variable or update this file"
        ],
        "free_tier": "1,000 requests/day"
    },
    "guardian": {
        "url": "https://bonobo.capi.gutools.co.uk/register/developer",
        "steps": [
            "1. Go to https://bonobo.capi.gutools.co.uk/register/developer",
            "2. Fill out the registration form",
            "3. Wait for approval (usually instant)",
            "4. Copy your API key",
            "5. Set GUARDIAN_API_KEY environment variable or update this file"
        ],
        "free_tier": "12,000 requests/day"
    },
    "newsdata": {
        "url": "https://newsdata.io/register", 
        "steps": [
            "1. Go to https://newsdata.io/register",
            "2. Create an account",
            "3. Verify your email",
            "4. Get your API key from dashboard",
            "5. Set NEWSDATA_API_KEY environment variable or update this file"
        ],
        "free_tier": "200 requests/day"
    }
}