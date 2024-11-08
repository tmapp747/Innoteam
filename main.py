import json
import os
from textwrap import dedent

from crewai import Agent, Crew, Task
from langchain.agents.agent_toolkits import FileManagementToolkit
from tasks import TaskPrompts

from tools.browser_tools import BrowserTools
from tools.file_tools import FileTools
from tools.search_tools import SearchTools

from flask import Flask, render_template, request, jsonify

# Add imports for Claude 3.5, Sonnet, and Deep Seek models
from langchain.llms import Claude, Sonnet, DeepSeek

app = Flask(__name__)

class ModernWebsiteCrew():
    def __init__(self, idea, llm=None):
        self.agents_config = json.loads(open("config/agents.json", "r").read())
        self.idea = idea
        self.llm = llm
        self.conversation_log = []
        self.__create_agents()

    def run(self):
        expanded_idea = self.__expand_idea()
        self.__setup_project()
        self.__create_website(expanded_idea)
        return "Website generated successfully!"

    def __expand_idea(self):
        expand_idea_task = Task(
            description=TaskPrompts.expand().format(idea=self.idea),
            agent=self.idea_analyst
        )
        refine_idea_task = Task(
            description=TaskPrompts.refine_idea(),
            agent=self.communications_strategist
        )
        crew = Crew(
            agents=[self.idea_analyst, self.communications_strategist],
            tasks=[expand_idea_task, refine_idea_task],
            verbose=True
        )
        expanded_idea = crew.kickoff()
        self.__log_conversation(crew)
        return expanded_idea

    def __setup_project(self):
        setup_task = Task(
            description="""
            Set up a modern web development project with the following requirements:
            1. Use Next.js 14 with App Router
            2. Implement Shadcn UI for beautiful components
            3. Use Tailwind CSS for styling
            4. Ensure responsive design
            5. Set up proper project structure with components, layouts, and pages
            6. Initialize git repository
            7. Set up proper TypeScript configuration
            
            Create the project in the 'website' directory.
            """,
            agent=self.web_developer
        )
        crew = Crew(
            agents=[self.web_developer],
            tasks=[setup_task],
            verbose=True
        )
        crew.kickoff()
        self.__log_conversation(crew)

    def __create_website(self, expanded_idea):
        create_components_task = Task(
            description=f"""
            Create modern, responsive website components based on the expanded idea:
            {expanded_idea}
            
            Requirements:
            1. Use Shadcn UI components
            2. Implement responsive design with Tailwind CSS
            3. Create reusable components
            4. Implement modern animations and transitions
            5. Ensure accessibility
            6. Add dark mode support
            7. Optimize for performance
            
            Components needed:
            - Hero section
            - Features section
            - About section
            - Contact form
            - Navigation
            - Footer
            """,
            agent=self.web_developer
        )
        
        create_content_task = Task(
            description=f"""
            Create compelling content for the website based on the expanded idea:
            {expanded_idea}
            
            Requirements:
            1. Write clear, engaging headlines
            2. Create persuasive call-to-actions
            3. Write concise feature descriptions
            4. Ensure consistent tone and voice
            5. Optimize for readability
            6. Include SEO-friendly content
            """,
            agent=self.content_editor
        )
        
        crew = Crew(
            agents=[self.web_developer, self.content_editor],
            tasks=[create_components_task, create_content_task],
            verbose=True
        )
        crew.kickoff()
        self.__log_conversation(crew)

    def __log_conversation(self, crew):
        for task in crew.tasks:
            for message in task.messages:
                self.conversation_log.append({
                    "agent": message.agent.name,
                    "role": message.agent.role,
                    "timestamp": message.timestamp,
                    "message": message.content
                })

    def __create_agents(self):
        idea_analyst_config = self.agents_config["senior_idea_analyst"]
        strategist_config = self.agents_config["senior_strategist"]
        developer_config = self.agents_config["senior_react_engineer"]
        editor_config = self.agents_config["senior_content_editor"]

        toolkit = FileManagementToolkit(
            root_dir='website',
            selected_tools=["read_file", "list_directory", "write_file"]
        )

        self.idea_analyst = Agent(
            **idea_analyst_config,
            verbose=True,
            llm=self.llm,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_kwebsite
            ]
        )

        self.communications_strategist = Agent(
            **strategist_config,
            verbose=True,
            llm=self.llm,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_kwebsite,
            ]
        )

        self.web_developer = Agent(
            **developer_config,
            verbose=True,
            llm=self.llm,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_kwebsite,
                FileTools.write_file
            ] + toolkit.get_tools()
        )

        self.content_editor = Agent(
            **editor_config,
            llm=self.llm,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_kwebsite,
            ]
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        idea = request.form['idea']
        llm = request.form.get('llm', None)
        api_key = request.form.get('api_key', None)

        # Handle new models
        if llm == 'claude':
            llm = Claude(api_key=api_key)
        elif llm == 'sonnet':
            llm = Sonnet(api_key=api_key)
        elif llm == 'deepseek':
            llm = DeepSeek(api_key=api_key)

        crew = ModernWebsiteCrew(idea, llm)
        result = crew.run()
        
        return jsonify({
            "message": result,
            "conversation_log": crew.conversation_log
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
