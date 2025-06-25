# Python Chatbot

A simple AI-powered chatbot web application built with Python (Flask), scikit-learn for basic intent classification, and a modern web frontend using HTML, JavaScript, and CSS.


## Features

- **Intelligent Intent Recognition**: Uses scikit-learn (TfidfVectorizer + LogisticRegression) to classify intents such as greetings, weather queries, and farewells.
- **Weather API Integration**: Responds with real weather data for a specified location using OpenWeatherMap (requires API key).
- **Extensible Intent Patterns**: Easily add new patterns/intents to expand chatbot capabilities.
- **Modern Chat UI**: Responsive frontend built with Bootstrap, custom CSS, and interactive JavaScript.
- **Stateless Web Chat**: Interact with the bot in your browser; messages are exchanged via AJAX.

## Project Structure

```
python_chatbot/
│
├── app.py              # Flask app with intent recognition and chat API
├── requirements.txt    # Python dependencies
├── static/
│   ├── js/
│   │   └── chat.js     # Frontend JavaScript for chat interactions
│   ├── css/
│   │   └── style.css   # Stylesheet for chat UI
│
├── templates/
│   └── index.html      # Main HTML page
└── README.md           # This file
```

## Setup & Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/kvasa02/python_chatbot.git
    cd python_chatbot
    ```

2. **Install Dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure API Keys (Optional for Weather)**
    - Edit `app.py` and set your OpenWeatherMap API key:
      ```python
      api_key = 'YOUR_API_KEY'
      ```
    - [Get a free API key here.](https://openweathermap.org/api)

4. **Run the Application**
    ```bash
    python app.py
    ```
    - The app will be available at [http://localhost:5000](http://localhost:5000).

## Usage

- Open your browser and go to [http://localhost:5000](http://localhost:5000)
- Type a message like:
  - `hello`
  - `weather in London`
  - `bye`
- The bot will reply based on recognized intent.

## Customizing Intents

- Edit the `intents` list in `app.py` to add or modify supported intents and their patterns.

## Example Intents

| Intent   | Example User Input          | Example Bot Reply                        |
|----------|----------------------------|------------------------------------------|
| greet    | `hello`, `hi`, `hey`       | Hello! How can I assist you today?       |
| weather  | `weather in Paris`         | Paris: clear sky, 22°C                   |
| bye      | `bye`, `goodbye`           | Goodbye! Have a nice day!                |

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [scikit-learn](https://scikit-learn.org/)
- [requests](https://docs.python-requests.org/)
- [Bootstrap 5](https://getbootstrap.com/) (CDN)
