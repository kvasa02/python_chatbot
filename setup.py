#!/usr/bin/env python3
"""
Setup script for the AI-Powered Chatbot
This script helps users install dependencies and configure the chatbot.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print a welcome banner"""
    print("=" * 60)
    print("🤖 AI-Powered Chatbot Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)

def install_spacy_model():
    """Install spaCy English model"""
    print("🧠 Installing spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing spaCy model")
        print("You can install it manually with: python -m spacy download en_core_web_sm")
        sys.exit(1)

def create_env_file():
    """Create .env file template"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("ℹ️  .env file already exists")
        return
    
    print("🔧 Creating .env file template...")
    env_content = """# API Keys for Enhanced Chatbot Features
# Get your API keys from the respective services:

# OpenWeatherMap API Key (for weather information)
# Sign up at: https://openweathermap.org/api
OPENWEATHER_API_KEY=your_openweather_api_key_here

# NewsAPI Key (for latest news)
# Sign up at: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here

# Optional: You can add more API keys here for additional features
# Example: GOOGLE_API_KEY=your_google_api_key_here
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("📝 Please edit the .env file with your API keys")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def check_api_keys():
    """Check if API keys are configured"""
    print("🔑 Checking API key configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    weather_key = os.getenv('OPENWEATHER_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    
    if not weather_key or weather_key == 'your_openweather_api_key_here':
        print("⚠️  OpenWeatherMap API key not configured")
        print("   Weather features will not work")
    else:
        print("✅ OpenWeatherMap API key configured")
    
    if not news_key or news_key == 'your_news_api_key_here':
        print("⚠️  NewsAPI key not configured")
        print("   News features will not work")
    else:
        print("✅ NewsAPI key configured")

def test_installation():
    """Test if the chatbot can be imported"""
    print("🧪 Testing installation...")
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not found - run: pip install flask")
        return False
    
    try:
        import spacy
        print("✅ spaCy imported successfully")
    except ImportError:
        print("❌ spaCy not found - run: pip install spacy")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn imported successfully")
    except ImportError:
        print("❌ scikit-learn not found - run: pip install scikit-learn")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError:
        print("❌ requests not found - run: pip install requests")
        return False
    
    try:
        import wikipedia
        print("✅ wikipedia imported successfully")
    except ImportError:
        print("❌ wikipedia not found - run: pip install wikipedia")
        return False
    
    try:
        from newsapi import NewsApiClient
        print("✅ newsapi imported successfully")
    except ImportError:
        print("❌ newsapi not found - run: pip install newsapi-python")
        return False
    
    print("✅ All required packages imported successfully")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit the .env file with your API keys (optional)")
    print("2. Run the chatbot: python app.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nAPI Key Setup:")
    print("- OpenWeatherMap: https://openweathermap.org/api")
    print("- NewsAPI: https://newsapi.org/")
    print("\nFor more information, see the README.md file")
    print("\nHappy Chatting! 🤖✨")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    print()
    
    # Install dependencies
    install_dependencies()
    print()
    
    # Install spaCy model
    install_spacy_model()
    print()
    
    # Create .env file
    create_env_file()
    print()
    
    # Test installation
    test_success = test_installation()
    print()
    
    # Check API keys
    check_api_keys()
    print()
    
    # Print next steps
    print_next_steps()
    
    if not test_success:
        print("\n⚠️  Some packages may not be installed correctly.")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 