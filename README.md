# ETA Agent System

An AI-driven system that automates anomaly-handling workflow for logistics and transportation.

## Features

- **Driver Agent**: Simulates chat with drivers to gather deviation information
- **User Agent**: Provides status updates and revised ETAs to customers
- **External API Integration**: Traffic and weather data validation
- **Role-based Routing**: Intelligent conversation routing based on user role
- **YAML-based Prompt Configuration**: Flexible and version-controlled prompt management
- **SQLite Database**: Lightweight, file-based database for easy deployment

## Project Structure

```
lesmes/
├── frontend/                          # Streamlit chat interface
├── backend/                           # FastAPI backend services
│   ├── app/
│   │   ├── config/                   # YAML prompt configurations
│   │   ├── models/                   # Database models (SQLite)
│   │   ├── services/                 # Agent services
│   │   ├── clients/                  # External API clients
│   │   └── api/                      # API endpoints
│   └── data/                         # SQLite database files
├── docker-compose.yml                # Container orchestration
└── .env                              # Environment configuration
```

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository>
   cd lesmes
   cp env.example .env
   # Edit .env with your API keys
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Configuration

The system uses YAML-based prompt configuration with version control:

- `backend/app/config/driver_agent.yml` - Driver interaction prompts
- `backend/app/config/user_agent.yml` - Customer interaction prompts

## API Endpoints

- `POST /api/conversation/route` - Route new conversations
- `POST /api/driver/chat` - Driver agent interaction
- `POST /api/user/chat` - User agent interaction
- `GET /api/status/{conversation_id}` - Get conversation status
- `POST /api/validate/eta` - Validate ETA with external APIs

## External APIs Used

- **Open-Meteo**: Free weather API (https://open-meteo.com/en/docs)
- **OpenRouteService**: Free traffic/routing API (https://openrouteservice.org/dev/#/api-docs)
- **OpenAI**: AI model for intelligent responses

## Development

See `DEVELOPMENT.md` for detailed development setup and guidelines.