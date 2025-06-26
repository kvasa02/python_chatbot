import re
import json
import os
import requests
import nltk
import spacy
from flask import Flask, request, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from dotenv import load_dotenv
import wikipedia
from newsapi import NewsApiClient
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

# Enhanced training data for intent classification
intents = [
    {
        'intent': 'greet',
        'patterns': [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'how are you', 'what\'s up', 'sup', 'yo', 'greetings'
        ],
        'responses': [
            'Hello! How can I assist you today?',
            'Hi there! What can I help you with?',
            'Hey! I\'m here to help. What do you need?',
            'Greetings! How may I be of service?'
        ]
    },
    {
        'intent': 'weather',
        'patterns': [
            'weather in', 'temperature at', 'forecast for', 'what\'s the weather',
            'how hot is it', 'how cold is it', 'weather today', 'temperature today',
            'is it raining', 'is it sunny', 'weather forecast'
        ],
        'responses': [
            'Let me check the weather for {entity}...',
            'I\'ll get the current weather conditions for {entity}.',
            'Checking the weather forecast for {entity}...'
        ]
    },
    {
        'intent': 'news',
        'patterns': [
            'news', 'latest news', 'current events', 'what\'s happening',
            'top headlines', 'breaking news', 'news today', 'recent news',
            'what\'s in the news', 'news headlines'
        ],
        'responses': [
            'Here are the latest news headlines...',
            'Let me get you the current news...',
            'Here\'s what\'s happening in the world...'
        ]
    },
    {
        'intent': 'search',
        'patterns': [
            'search for', 'find information about', 'tell me about', 'what is',
            'who is', 'define', 'explain', 'information about', 'look up'
        ],
        'responses': [
            'Let me search for information about {entity}...',
            'I\'ll find information about {entity} for you.',
            'Searching for details about {entity}...'
        ]
    },
    {
        'intent': 'joke',
        'patterns': [
            'tell me a joke', 'say something funny', 'make me laugh',
            'joke', 'funny', 'humor', 'comedy'
        ],
        'responses': [
            'Here\'s a joke for you: Why don\'t scientists trust atoms? Because they make up everything!',
            'Why did the scarecrow win an award? Because he was outstanding in his field!',
            'What do you call a fake noodle? An impasta!'
        ]
    },
    {
        'intent': 'bye',
        'patterns': [
            'bye', 'goodbye', 'see you', 'farewell', 'take care',
            'have a good day', 'see you later', 'good night'
        ],
        'responses': [
            'Goodbye! Have a nice day!',
            'See you later! Take care!',
            'Farewell! Come back anytime!',
            'Goodbye! It was nice chatting with you!'
        ]
    },
    {
        'intent': 'help',
        'patterns': [
            'help', 'what can you do', 'capabilities', 'features',
            'how do you work', 'what are your functions', 'assist me'
        ],
        'responses': [
            'I can help you with:\n• Weather information\n• Latest news\n• Search for information\n• Tell jokes\n• General conversation\nJust ask me anything!',
            'Here\'s what I can do:\n• Check weather for any location\n• Get the latest news headlines\n• Search for information on topics\n• Share some jokes\n• Have a friendly chat'
        ]
    }
]

class EnhancedChatbot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = MultinomialNB()
        self.train_model()
        
    def train_model(self):
        """Train the intent classification model"""
        X_train = []
        y_train = []
        
        for intent_data in intents:
            for pattern in intent_data['patterns']:
                X_train.append(pattern)
                y_train.append(intent_data['intent'])
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.classifier.fit(X_train_vec, y_train)
    
    def classify_intent(self, text):
        """Classify the intent of user input"""
        text_vec = self.vectorizer.transform([text])
        return self.classifier.predict(text_vec)[0]
    
    def extract_entities(self, text):
        """Extract entities using spaCy NER"""
        entities = {}
        
        if nlp:
            doc = nlp(text.lower())
            
            # Extract location entities
            locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
            if locations:
                entities['location'] = locations[0]
            
            # Extract person entities
            persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
            if persons:
                entities['person'] = persons[0]
            
            # Extract organization entities
            orgs = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
            if orgs:
                entities['organization'] = orgs[0]
        
        # Fallback regex patterns for entity extraction
        if 'location' not in entities:
            # Weather location extraction
            weather_match = re.search(r'(?:weather|temperature|forecast)\s+(?:in|at|for)\s+([A-Za-z\s]+)', text, re.IGNORECASE)
            if weather_match:
                entities['location'] = weather_match.group(1).strip()
        
        if 'search_term' not in entities:
            # Search term extraction
            search_match = re.search(r'(?:search for|find|tell me about|what is|who is)\s+([A-Za-z\s]+)', text, re.IGNORECASE)
            if search_match:
                entities['search_term'] = search_match.group(1).strip()
        
        return entities
    
    def get_weather(self, city):
        """Get weather information using OpenWeatherMap API"""
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if not api_key:
            return "Weather API key not configured. Please set OPENWEATHER_API_KEY in your environment variables."
        
        if not city:
            return "Please specify a location for the weather query."
        
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("cod") == "404":
                return f"Sorry, I couldn't find weather information for '{city}'. Please check the spelling."
            
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            
            return (
                f"🌤️ Weather in {city_name}:\n"
                f"• Condition: {description.title()}\n"
                f"• Temperature: {temp}°C (feels like {feels_like}°C)\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_speed} m/s"
            )
            
        except Exception as e:
            return f"Sorry, I couldn't fetch weather data for {city}. Please try again later."
    
    def get_news(self, category='general', country='us'):
        """Get latest news using NewsAPI"""
        api_key = os.getenv('NEWS_API_KEY')
        
        if not api_key:
            return "News API key not configured. Please set NEWS_API_KEY in your environment variables."
        
        try:
            newsapi = NewsApiClient(api_key=api_key)
            top_headlines = newsapi.get_top_headlines(category=category, country=country, page_size=5)
            
            if not top_headlines['articles']:
                return "Sorry, I couldn't fetch the latest news right now."
            
            news_text = "📰 Latest Headlines:\n\n"
            for i, article in enumerate(top_headlines['articles'], 1):
                title = article['title']
                source = article['source']['name']
                news_text += f"{i}. {title}\n   Source: {source}\n\n"
            
            return news_text
            
        except Exception as e:
            return "Sorry, I couldn't fetch the latest news right now. Please try again later."
    
    def search_wikipedia(self, query):
        """Search for information using Wikipedia API"""
        try:
            # Search for the topic
            search_results = wikipedia.search(query, results=3)
            
            if not search_results:
                return f"Sorry, I couldn't find information about '{query}'."
            
            # Get the summary of the first result
            page = wikipedia.page(search_results[0])
            summary = wikipedia.summary(search_results[0], sentences=3)
            
            return f"📚 Information about {query}:\n\n{summary}\n\nSource: Wikipedia"
            
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found for '{query}'. Please be more specific."
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find information about '{query}'."
        except Exception as e:
            return f"Sorry, I couldn't search for '{query}' right now."
    
    def generate_response(self, user_input):
        """Generate response based on intent and entities"""
        intent = self.classify_intent(user_input.lower())
        entities = self.extract_entities(user_input)
        
        # Find the intent data
        intent_data = next((intent_item for intent_item in intents if intent_item['intent'] == intent), None)
        
        if not intent_data:
            return "I'm sorry, I didn't understand that. Try asking for help to see what I can do!"
        
        # Handle specific intents
        if intent == 'weather':
            location = entities.get('location')
            if location:
                return self.get_weather(location)
            else:
                return "Please specify a location for the weather query (e.g., 'weather in London')."
        
        elif intent == 'news':
            return self.get_news()
        
        elif intent == 'search':
            search_term = entities.get('search_term')
            if search_term:
                return self.search_wikipedia(search_term)
            else:
                return "Please specify what you'd like me to search for (e.g., 'tell me about Python programming')."
        
        elif intent == 'joke':
            return random.choice(intent_data['responses'])
        
        elif intent == 'help':
            return random.choice(intent_data['responses'])
        
        elif intent == 'bye':
            return random.choice(intent_data['responses'])
        
        elif intent == 'greet':
            return random.choice(intent_data['responses'])
        
        else:
            return "I'm sorry, I didn't understand that. You can ask me about weather, news, search for information, or just say hi!"

# Initialize chatbot
chatbot = EnhancedChatbot()

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        
        if not user_input.strip():
            return jsonify({'response': 'Please enter a message.'})
        
        bot_response = chatbot.generate_response(user_input)
        return jsonify({'response': bot_response})
        
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong. Please try again.'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
