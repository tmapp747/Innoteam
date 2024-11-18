<<<<<<< HEAD
# Innodev Crew for Website Development
## Introduction
This project is an example using the Innodev Team framework to automate the process of creating landing pages from a single idea. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.
=======
# Innoteam Website Generator
>>>>>>> main

A modern web application that generates websites using AI-powered agents and modern web technologies.

## Features

- **AI-Powered Website Generation**
  - Multiple LLM support (Claude, Sonnet, DeepSeek)
  - Intelligent idea expansion and refinement
  - Modern component generation using Next.js and Shadcn UI
  - SEO-optimized content creation

- **User Management**
  - Secure authentication system
  - API key management
  - User dashboard
  - Website management

- **API Integration**
  - RESTful API endpoints
  - API key authentication
  - Rate limiting
  - Comprehensive documentation

- **Security Features**
  - JWT authentication
  - CSRF protection
  - Rate limiting
  - Secure password handling
  - Input validation

- **Modern Architecture**
  - Flask application factory pattern
  - Blueprint-based organization
  - SQLAlchemy ORM
  - Redis caching (optional)
  - Comprehensive logging

## Tech Stack

- **Backend**
  - Flask
  - SQLAlchemy
  - Flask-Login
  - Flask-Migrate
  - Flask-Limiter
  - Flask-CORS
  - Flask-Caching

- **Frontend Generation**
  - Next.js 14
  - Shadcn UI
  - Tailwind CSS
  - TypeScript

- **AI/ML**
  - CrewAI
  - LangChain
  - Multiple LLM support

- **Database**
  - SQLite (development)
  - PostgreSQL (production)

- **Caching**
  - Redis (optional)

## Installation

1. Clone the repository:

   ```bash
```bash
   git clone https://github.com/yourusername/innoteam.git
   cd innoteam
   ```  

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
  ```plaintext

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

## Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run tests:
   ```bash
   pytest
   ```

4. Format code:
   ```bash
   black .
   ```

## API Documentation

The API documentation is available at `/api/docs` when running the application. Key endpoints include:

- `POST /api/v1/websites` - Generate a new website
- `GET /api/v1/websites` - List all websites
- `GET /api/v1/websites/<id>` - Get website details
- `DELETE /api/v1/websites/<id>` - Delete a website
- `POST /api/v1/websites/<id>/regenerate` - Regenerate a website

## Environment Variables

Key environment variables for configuration:

- `FLASK_ENV` - Application environment (development/production)
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection URL
- `REDIS_URL` - Redis connection URL (optional)
- `CLAUDE_API_KEY` - Claude API key
- `SONNET_API_KEY` - Sonnet API key
- `DEEPSEEK_API_KEY` - DeepSeek API key

See `.env.example` for all available configuration options.

## Project Structure

```
innoteam/
├── app/
│   ├── api/            # API endpoints
│   ├── auth/           # Authentication
│   ├── core/           # Core functionality
│   ├── models/         # Database models
│   ├── templates/      # HTML templates
│   ├── static/         # Static files
│   └── utils/          # Utilities
├── config/             # Configuration files
├── logs/               # Application logs
├── tests/              # Test suite
├── .env                # Environment variables
├── requirements.txt    # Dependencies
└── run.py             # Application entry
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

