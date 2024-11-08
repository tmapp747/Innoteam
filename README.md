# AI Crew for Landing Pages

## Introduction
This project is an example using the CrewAI framework to automate the process of creating landing pages from a single idea. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

*Disclaimer: Templates are not included as they are Tailwind templates. Place Tailwind individual template folders in `./templates`, if you have a license you can download them at (https://tailwindui.com/templates), their references are at `config/templates.json`, this was not tested with other templates, prompts in `tasks.py` might require some changes for that to work.*

By [@joaomdmoura](https://x.com/joaomdmoura)

## Table of Contents
- [Quick Start Guide](#quick-start-guide)
- [Detailed Setup Instructions](#detailed-setup-instructions)
- [CrewAI Framework](#crewai-framework)
- [Running the Script](#running-the-script)
- [CI/CD Pipeline](#ci-cd-pipeline)
- [Deployment Guide](#deployment-guide)
- [Project Structure](#project-structure)
- [Using GPT 3.5](#using-gpt-35)
- [Using Local Models with Ollama](#using-local-models-with-ollama)
- [Contributing](#contributing)
- [Support and Contact](#support-and-contact)
- [License](#license)
- [Analyzing for Improvements](#analyzing-for-improvements)

## Quick Start Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Innoteam.git
   cd Innoteam
   ```

2. Install dependencies:
   ```bash
   poetry lock && poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Detailed Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Poetry package manager
- Node.js 18+ (for website)
- Git

### Environment Setup
1. Configure API keys for:
   - [Browserless](https://www.browserless.io/)
   - [Serper](https://serper.dev/)
   - [OpenAI](https://platform.openai.com/api-keys)

2. Add Tailwind Templates:
   - Place template folders in `./templates`
   - Update references in `config/templates.json`

### Development Environment
1. Install Python dependencies:
   ```bash
   poetry install
   ```

2. Install website dependencies:
   ```bash
   cd website
   npm install
   ```

3. Start development servers:
   - Backend:
     ```bash
     poetry run python main.py
     ```
   - Frontend:
     ```bash
     cd website
     npm run dev
     ```

## CI/CD Pipeline

Our project includes a comprehensive CI/CD pipeline using GitHub Actions that automates testing, building, and deployment processes.

### Pipeline Features
- Automated testing on every push and pull request
- Automatic deployment to production for main branch
- Separate deployment pipelines for frontend and backend
- Built-in security checks and dependency updates

### Pipeline Structure
1. **Build and Test**
   - Runs Python tests
   - Builds frontend application
   - Checks code quality

2. **Backend Deployment (Heroku)**
   - Automatically deploys to Heroku on main branch
   - Handles database migrations
   - Updates environment variables

3. **Frontend Deployment (Vercel)**
   - Deploys website to Vercel
   - Optimizes assets
   - Updates configurations

## Deployment Guide

### Backend Deployment (Heroku)
1. Create a Heroku account
2. Install Heroku CLI
3. Create new Heroku app:
   ```bash
   heroku create your-app-name
   ```
4. Add GitHub Secrets:
   - HEROKU_API_KEY
   - HEROKU_APP_NAME
   - HEROKU_EMAIL

### Frontend Deployment (Vercel)
1. Create a Vercel account
2. Link GitHub repository
3. Add GitHub Secrets:
   - VERCEL_TOKEN
   - VERCEL_ORG_ID
   - VERCEL_PROJECT_ID

### Manual Deployment
If needed, you can manually deploy:

Backend:
```bash
git push heroku main
```

Frontend:
```bash
cd website
vercel deploy
```

## Project Structure
```
.
├── .github/workflows/    # CI/CD configuration
├── config/              # Configuration files
├── main-files/          # Core application files
├── tools/               # Utility tools
├── website/             # Frontend application
├── main.py             # Main application entry
├── tasks.py            # Task definitions
└── README.md           # Documentation
```

## CrewAI Framework
CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to transform an idea into a fully fleshed-out landing page by expanding the idea, choosing a template, and customizing it to fit the concept.

## Running the Script
It uses GPT-4 by default so you should have access to that to run it.

***Disclaimer:** This will use gpt-4 unless you changed it 
not to, and by doing so it will cost you money (~2-9 USD).
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
