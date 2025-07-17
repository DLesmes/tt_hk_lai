# ETA Agent System Documentation

## 🚚 Overview

The ETA Agent System is an AI-driven logistics anomaly handling and ETA optimization platform. It provides intelligent chat-based interactions for both logistics users and drivers, with real-time integration to weather and traffic APIs for accurate ETA predictions.

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│  (Weather/Traffic)│
│                 │    │                 │    │                 │
│ • Chat Interface│    │ • Agent Services│    │ • Open-Meteo    │
│ • Agent Selection│   │ • OpenAI Client │    │ • OpenRouteService│
│ • System Status │    │ • Database      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **AI**: OpenAI GPT-4 (via LangChain)
- **External APIs**: Open-Meteo (Weather), OpenRouteService (Traffic)
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API Key
- OpenRouteService API Key (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lesmes
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start the system**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 User Guide

### Frontend Interface

#### Main Features

1. **Agent Selection**
   - Choose between "User" and "Driver" agents
   - Each agent has specialized capabilities

2. **Chat Interface**
   - Real-time messaging with AI agents
   - Message history and conversation persistence
   - System status indicators

3. **System Status**
   - Real-time health monitoring
   - Backend connectivity status
   - External API status

#### Using the Chat Interface

1. **Select an Agent Type**
   - **User Agent**: For logistics analysis, customer support, and ETA optimization
   - **Driver Agent**: For route optimization, incident reporting, and real-time updates

2. **Send Messages**
   - Type your message in the text area
   - Click "Send" or press Enter
   - Wait for AI response

3. **View Responses**
   - Agent responses appear in purple bubbles
   - System messages appear in orange bubbles
   - Your messages appear in blue bubbles

### Agent Capabilities

#### User Agent
- 📊 Analyze logistics data and ETA reports
- 🚨 Handle anomaly detection and resolution
- 📈 Provide optimization recommendations
- 🔍 Investigate delivery issues
- 📋 Generate reports and summaries

#### Driver Agent
- 🚗 Real-time route optimization
- ⚡ Traffic and weather integration
- 🛣️ Dynamic ETA updates
- 🚨 Incident reporting and handling
- 📱 Mobile-friendly interactions

## 🔧 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "debug": true
}
```

#### Chat Endpoint
```http
POST /chat
```

**Request Body:**
```json
{
  "message": "Your message here",
  "agent_type": "user|driver",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "response": "AI agent response",
  "conversation_id": "generated-conversation-id",
  "system_info": "Processed by user agent",
  "metadata": {
    "model_info": {},
    "timestamp": "2025-07-16T23:54:52.078174"
  }
}
```

#### API Status
```http
GET /api/status
```

**Response:**
```json
{
  "api": "ETA Agent System",
  "version": "0.1.0",
  "database": "SQLite",
  "ai_model": "gpt-4",
  "environment": "development"
}
```

#### Weather API Test
```http
GET /weather/test
```

#### Traffic API Test
```http
GET /traffic/test
```

## 🧪 Testing

### Running Tests

1. **Install test dependencies**
   ```bash
   pip install -r tests/requirements.txt
   ```

2. **Run all tests**
   ```bash
   python run_tests.py
   ```

3. **Run specific test suites**
   ```bash
   # Backend tests only
   pytest tests/test_backend.py -v
   
   # Frontend tests only
   pytest tests/test_frontend.py -v
   
   # Quick system test
   python test_frontend.py
   ```

### Test Coverage

The test suite covers:
- ✅ API endpoint functionality
- ✅ Agent service responses
- ✅ External API integrations
- ✅ Error handling
- ✅ Performance metrics
- ✅ Frontend-backend integration

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENROUTESERVICE_API_KEY` | OpenRouteService API key | Optional |
| `DEBUG` | Enable debug mode | `True` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Environment name | `development` |

### Frontend Configuration

Key configuration files:
- `frontend/config.py`: UI settings and styling
- `frontend/utils.py`: Utility functions
- `frontend/components.py`: UI components

### Backend Configuration

Key configuration files:
- `backend/app/settings.py`: Application settings
- `backend/app/config/`: Configuration modules
- `backend/app/services/`: Agent services

## 🚀 Deployment

### Production Deployment

1. **Update environment variables**
   ```bash
   ENVIRONMENT=production
   DEBUG=False
   LOG_LEVEL=WARNING
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up reverse proxy** (recommended)
   - Use Nginx or Apache
   - Configure SSL certificates
   - Set up load balancing

### Monitoring

- **Health checks**: `/health` endpoint
- **Logs**: Docker container logs
- **Metrics**: Built-in performance tracking

## 🔒 Security

### API Security
- Input validation on all endpoints
- Rate limiting (recommended for production)
- CORS configuration
- Error message sanitization

### Data Security
- SQLite database with proper permissions
- Environment variable management
- API key rotation

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check API keys in `.env`
   - Verify Docker is running
   - Check container logs: `docker-compose logs backend`

2. **Frontend not accessible**
   - Verify port 8501 is available
   - Check container logs: `docker-compose logs frontend`
   - Ensure backend is healthy

3. **Chat not working**
   - Verify OpenAI API key is valid
   - Check backend logs for errors
   - Test API directly: `curl -X POST http://localhost:8000/chat`

4. **External APIs failing**
   - Check API keys
   - Verify internet connectivity
   - Review API rate limits

### Debug Commands

```bash
# Check system status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Test API directly
curl http://localhost:8000/health

# Run quick test
python test_frontend.py
```

## 📈 Performance

### Optimization Tips

1. **Response Time**
   - Average response time: < 30 seconds
   - Concurrent request handling: 5+ requests
   - Memory usage: ~512MB per container

2. **Scaling**
   - Horizontal scaling with load balancer
   - Database connection pooling
   - Caching for external API responses

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Run tests**
5. **Submit pull request**

### Code Standards

- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Use type hints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Run the test suite
- Check container logs

---

**ETA Agent System v0.1.0** - AI-driven logistics optimization platform 