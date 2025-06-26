"""
Configuration file for the Enhanced AI Chatbot
Set your API keys and other configuration options here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the chatbot"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Chatbot Configuration
    MAX_RESPONSE_LENGTH = 1000
    DEFAULT_COUNTRY = 'us'
    DEFAULT_NEWS_CATEGORY = 'general'
    
    # NLP Configuration
    SPACY_MODEL = 'en_core_web_sm'
    TFIDF_MAX_FEATURES = 1000
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that required API keys are set"""
        missing_keys = []
        
        if not cls.OPENWEATHER_API_KEY:
            missing_keys.append('OPENWEATHER_API_KEY')
        
        if not cls.NEWS_API_KEY:
            missing_keys.append('NEWS_API_KEY')
        
        if missing_keys:
            print("⚠️  Warning: The following API keys are not set:")
            for key in missing_keys:
                print(f"   - {key}")
            print("\nSome features may not work without these API keys.")
            print("Please set them in your .env file or environment variables.")
            print("\nTo get API keys:")
            print("- OpenWeatherMap: https://openweathermap.org/api")
            print("- NewsAPI: https://newsapi.org/")
        
        return len(missing_keys) == 0 