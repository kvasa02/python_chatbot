import re
import requests
from flask import Flask, request, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data for intent classification
intents = [
    {'intent': 'greet', 'patterns': ['hello', 'hi', 'hey'], 'response': 'Hello! How can I assist you today?'},
    {'intent': 'weather', 'patterns': ['weather in', 'temperature at', 'forecast for'], 'response': 'Fetching weather for {entity}...'},
    {'intent': 'bye', 'patterns': ['bye', 'goodbye', 'see you'], 'response': 'Goodbye! Have a nice day!'}
]

# Prepare data
X_train = [p for intent in intents for p in intent['patterns']]
y_train = [intent['intent'] for intent in intents for _ in intent['patterns']]

# Train simple intent classifier
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
clf = LogisticRegression().fit(X_train_vec, y_train)

def classify_intent(text):
    vec = vectorizer.transform([text])
    return clf.predict(vec)[0]

def extract_entity(text):
    # Simple entity extraction for a location in weather queries
    # This regex tries to find a phrase after 'in', 'at', or 'for'
    match = re.search(r'(?:in|at|for)\s+([A-Za-z\s]+)', text, re.IGNORECASE)
    if match:
        # Take the matched group and strip any leading/trailing whitespace
        entity = match.group(1).strip()
        # Basic cleaning: remove common weather query words from the end
        if entity.lower().endswith(('weather', 'temperature', 'forecast')):
            entity = re.sub(r'\s*(weather|temperature|forecast)$', '', entity, flags=re.IGNORECASE).strip()
        return entity
    return None

def get_weather(city):
    """
    Fetches real-time weather information using OpenWeatherMap API.
    """
    # --- IMPORTANT: Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API Key ---
    api_key = '9266c00413f6ef213904ad90f654be1e'  # <--- REPLACE THIS LINE WITH YOUR KEY
    # ---------------------------------------------------------------------------------

    if not api_key or api_key == '9266c00413f6ef213904ad90f654be1e':
        return "Weather API key not set. Please update the code with your OpenWeatherMap API key."
    
    if not city:
        return "Please specify a location for the weather (e.g., 'weather in London')."

    # Base URL for OpenWeatherMap Current Weather Data API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric' # 'units=metric' for Celsius

    try:
        res = requests.get(url)
        res.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = res.json()

        # Check for OpenWeatherMap specific error codes (e.g., city not found)
        if data.get("cod") == "404":
            return f"Sorry, I couldn't find weather information for '{city}'. Please check the spelling or try a nearby major city."
        elif data.get("cod") == 401: # 401 Unauthorized likely due to invalid API key
            return "There's an issue with the OpenWeatherMap API key. Please check if it's correct and valid."

        # Extract relevant weather details
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        city_name_from_api = data['name'] # Get the official city name from the API response

        return (
            f"The weather in {city_name_from_api} is {description}. "
            f"Temperature: {temp}°C (feels like {feels_like}°C). "
            f"Humidity: {humidity}%."
        )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {res.text if res else 'No response'}")
        return "An HTTP error occurred while fetching weather data. Please try again later."
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return "Could not connect to the weather service. Please check your internet connection."
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return "The request to the weather service timed out. Please try again later."
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
        return "I'm having trouble fetching weather information right now. Please try again later."
    except KeyError as key_err:
        print(f"KeyError in weather data: {key_err} - Data: {data}")
        return f"Could not parse weather data for '{city}'. The structure might have changed or data is missing."
    except Exception as e:
        print(f"An unexpected error occurred in get_weather: {e}")
        return "An unexpected error occurred while processing the weather request."


def generate_response(user_input):
    intent = classify_intent(user_input.lower())
    for intent_data in intents:
        if intent_data['intent'] == intent:
            if intent == 'weather':
                entity = extract_entity(user_input.lower()) # Pass lowercased input to extract_entity
                if entity:
                    return get_weather(entity)
                else:
                    return "Please specify a location for the weather query (e.g., 'weather in London')."
            else:
                return intent_data['response']
    return "I'm sorry, I didn't understand that. You can ask about weather, or say hi/bye."

# Flask Web Interface
app = Flask(__name__)

@app.route("/")
def home():
    # Use your existing index.html
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    bot_response = generate_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
