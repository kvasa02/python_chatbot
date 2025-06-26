# 🤖 AI-Powered Chatbot with Natural Language Processing

A sophisticated AI chatbot built with Python, Flask, and advanced NLP techniques. This chatbot features intent classification, entity recognition, and integration with multiple external APIs for real-time responses.

## ✨ Features

### 🧠 Natural Language Processing (NLP)
- **Intent Classification**: Uses TF-IDF vectorization and Naive Bayes classification to understand user intent
- **Entity Recognition**: Leverages spaCy NER to extract locations, persons, and organizations from text
- **Pattern Matching**: Advanced regex patterns for fallback entity extraction
- **Context Understanding**: Multi-turn conversation support with context awareness

### 🌐 External API Integrations
- **Weather Information**: Real-time weather data via OpenWeatherMap API
- **News Headlines**: Latest news via NewsAPI
- **Information Search**: Wikipedia integration for detailed topic information
- **Extensible Architecture**: Easy to add more API integrations

### 🎨 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Chat**: Live typing indicators and smooth animations
- **Smart Suggestions**: Quick action buttons for common queries
- **Beautiful UI**: Modern gradient design with smooth interactions

### 🔧 Technical Features
- **Flask Web Framework**: Robust backend with RESTful API
- **Error Handling**: Comprehensive error handling and user feedback
- **Environment Configuration**: Secure API key management
- **Scalable Architecture**: Object-oriented design for easy maintenance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python_chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up API keys** (Optional but recommended)
   
   Create a `.env` file in the project root:
   ```env
   # Weather API (OpenWeatherMap)
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   
   # News API
   NEWS_API_KEY=your_news_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔑 API Key Setup

### OpenWeatherMap API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as `OPENWEATHER_API_KEY`

### NewsAPI
1. Visit [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as `NEWS_API_KEY`

## 💬 Usage Examples

### Weather Queries
- "What's the weather in London?"
- "Temperature in New York"
- "Weather forecast for Tokyo"

### News Queries
- "Show me the latest news"
- "What's happening in the world?"
- "Breaking news"

### Information Search
- "Tell me about Python programming"
- "Who is Albert Einstein?"
- "What is machine learning?"

### General Conversation
- "Hello" / "Hi" / "Hey"
- "Tell me a joke"
- "What can you do?"
- "Goodbye"

## 🏗️ Architecture

### Backend Structure
```
app.py              # Main Flask application
config.py           # Configuration management
requirements.txt    # Python dependencies
```

### Frontend Structure
```
templates/
├── index.html      # Main chat interface
static/
├── css/
│   └── style.css   # Styling and animations
└── js/
    └── chat.js     # Frontend functionality
```

### Key Components

#### EnhancedChatbot Class
- **Intent Classification**: TF-IDF + Naive Bayes
- **Entity Recognition**: spaCy NER + Regex fallback
- **Response Generation**: Context-aware responses
- **API Integration**: Weather, News, Wikipedia

#### Frontend Interface
- **Real-time Chat**: WebSocket-like experience
- **Typing Indicators**: Visual feedback
- **Responsive Design**: Mobile-first approach
- **Accessibility**: Keyboard shortcuts and screen reader support

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | No | None |
| `NEWS_API_KEY` | NewsAPI key | No | None |
| `DEBUG` | Flask debug mode | No | True |
| `SECRET_KEY` | Flask secret key | No | Auto-generated |

### Customization
You can easily customize the chatbot by:

1. **Adding new intents** in the `intents` list in `app.py`
2. **Integrating new APIs** by adding methods to the `EnhancedChatbot` class
3. **Modifying the UI** by editing the CSS and HTML files
4. **Training custom models** by replacing the current NLP pipeline

## 🧪 Testing

### Manual Testing
1. Start the application
2. Try various queries in the chat interface
3. Test error scenarios (invalid API keys, network issues)
4. Verify responsive design on different screen sizes

### API Testing
```bash
# Test the chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `DEBUG=False` in environment variables
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up proper environment variables
4. Configure reverse proxy (Nginx, Apache)

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- [spaCy](https://spacy.io/) for NLP capabilities
- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [NewsAPI](https://newsapi.org/) for news headlines
- [Wikipedia](https://wikipedia.org/) for information search
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section below
2. Review the error logs
3. Open an issue on GitHub

## 🔧 Troubleshooting

### Common Issues

**spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**API key errors**
- Verify your API keys are correctly set in the `.env` file
- Check that the APIs are accessible from your network
- Ensure you have sufficient API credits

**Import errors**
```bash
pip install -r requirements.txt --upgrade
```

**Port already in use**
```bash
# Change the port in app.py or kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

---

**Happy Chatting! 🤖✨**
