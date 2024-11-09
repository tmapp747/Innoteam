# Innoteam Website Generator

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
   git clone https://github.com/yourusername/innoteam.git
   cd innoteam
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

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
The full run might take around ~10-45m. Enjoy your time back*

## Using GPT 3.5
CrewAI allows you to pass an llm argument to the agent constructor, that will be its brain, so changing the agent to use GPT-3.5 instead of GPT-4 is as simple as passing that argument on the agent you want to use that LLM (in `main.py`).
```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model='gpt-3.5') # Loading GPT-3.5

self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=llm, # <----- passing our llm reference here
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_kwebsite
    ]
)
```

## Using Local Models with Ollama
The CrewAI framework supports integration with local models, such as Ollama, for enhanced flexibility and customization. This allows you to utilize your own models, which can be particularly useful for specialized tasks or data privacy concerns.

### Setting Up Ollama
- **Install Ollama**: Ensure that Ollama is properly installed in your environment. Follow the installation guide provided by Ollama for detailed instructions.
- **Configure Ollama**: Set up Ollama to work with your local model. You will probably need to tweak the model using a Modelfile, an example of which is provided in the root folder (Openhermes25Modelfile) for the OpenHermes2.5 which is super light and works great. You can use the Modelfile once you have the model installed with `ollama create agent -f OpenHermes25Modelfile`.

### Integrating Ollama with CrewAI
```python
from langchain.llms import Ollama
ollama_openhermes = Ollama(model="agent")

self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=ollama_openhermes, # Ollama model passed here
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website
    ]
)
```

### Advantages of Using Local Models
- **Privacy**: Local models allow processing of data within your own infrastructure, ensuring data privacy.
- **Customization**: You can customize the model to better suit the specific needs of your tasks.
- **Performance**: Depending on your setup, local models can offer performance benefits, especially in terms of latency.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support and Contact
For support, please open an issue in the GitHub repository.

## License
This project is released under the MIT License.

## Analyzing for Improvements

### Overview
This section provides guidelines on how to analyze the project for potential improvements. It includes steps to review the code, identify areas for enhancement, and implement changes.

### Steps to Analyze for Improvements
1. **Review Code Quality**: Check for code readability, maintainability, and adherence to coding standards.
2. **Identify Performance Bottlenecks**: Use profiling tools to identify slow parts of the code and optimize them.
3. **Check for Security Vulnerabilities**: Perform security audits to identify and fix potential vulnerabilities.
4. **Evaluate User Experience**: Gather user feedback and analyze the user interface for improvements.
5. **Update Dependencies**: Ensure all dependencies are up-to-date and compatible with the project.

### Running the Analysis Task
To run the new task prompt for analyzing and suggesting improvements, follow these steps:

1. **Navigate to the project directory**:
   ```bash
   cd Innoteam
   ```

2. **Run the analysis task**:
   ```bash
   python main.py --task analyze_improvements
   ```

3. **Review the output**: The task will generate a report detailing the suggested improvements and areas for enhancement.
