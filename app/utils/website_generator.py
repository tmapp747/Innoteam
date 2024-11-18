import json
import os
from datetime import datetime
from flask import current_app
from crewai import Agent, Crew, Task
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.llms import Claude, Sonnet, DeepSeek

class ModernWebsiteCrew:
    def __init__(self, idea, llm_type=None, api_key=None, website_id=None):
        self.idea = idea
        self.website_id = website_id
        self.conversation_log = []
        self.output_dir = os.path.join(current_app.static_folder, f'generated/website_{website_id}')
        
        # Initialize LLM based on type
        if llm_type == 'claude' and api_key:
            self.llm = Claude(api_key=api_key)
        elif llm_type == 'sonnet' and api_key:
            self.llm = Sonnet(api_key=api_key)
        elif llm_type == 'deepseek' and api_key:
            self.llm = DeepSeek(api_key=api_key)
        else:
            self.llm = None  # Default to environment configuration
            
        self.__load_agents_config()
        self.__create_agents()
        self.__ensure_output_directory()

    def run(self):
        """Execute the website generation process"""
        try:
            expanded_idea = self.__expand_idea()
            self.__setup_project()
            self.__create_website(expanded_idea)
            return "Website generated successfully!"
        except Exception as e:
            current_app.logger.error(f"Website generation error: {str(e)}")
            raise

    def __load_agents_config(self):
        """Load agent configurations"""
        config_path = os.path.join(current_app.root_path, 'config', 'agents.json')
        with open(config_path, 'r') as f:
            self.agents_config = json.load(f)

    def __ensure_output_directory(self):
        """Ensure the output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)

    def __expand_idea(self):
        """Expand the initial website idea"""
        expand_task = Task(
            description=f"""
            Analyze and expand upon the following website idea:
            {self.idea}
            
            Consider:
            1. Target audience and their needs
            2. Key features and functionality
            3. Content structure and organization
            4. Visual design elements
            5. Technical requirements
            6. SEO considerations
            
            Provide a detailed expansion of the idea.
            """,
            agent=self.idea_analyst
        )
        
        refine_task = Task(
            description="""
            Refine the expanded idea focusing on:
            1. User experience and journey
            2. Content strategy
            3. Call-to-actions
            4. Performance optimization
            5. Mobile responsiveness
            6. Accessibility requirements
            
            Provide a refined implementation plan.
            """,
            agent=self.communications_strategist
        )
        
        crew = Crew(
            agents=[self.idea_analyst, self.communications_strategist],
            tasks=[expand_task, refine_task],
            verbose=True
        )
        
        result = crew.kickoff()
        self.__log_conversation(crew)
        return result

    def __setup_project(self):
        """Set up the website project structure"""
        setup_task = Task(
            description=f"""
            Set up a modern web development project in {self.output_dir} with:
            1. Next.js 14 with App Router
            2. Shadcn UI components
            3. Tailwind CSS
            4. TypeScript configuration
            5. ESLint and Prettier
            6. Git initialization
            7. Responsive design setup
            8. Dark mode support
            
            Create a clean, maintainable project structure.
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
        """Create the website components and content"""
        create_components_task = Task(
            description=f"""
            Create modern website components based on:
            {expanded_idea}
            
            Requirements:
            1. Use Shadcn UI components
            2. Implement responsive Tailwind CSS
            3. Create reusable components
            4. Add animations and transitions
            5. Ensure accessibility
            6. Optimize performance
            7. Support dark mode
            
            Output directory: {self.output_dir}
            """,
            agent=self.web_developer
        )
        
        create_content_task = Task(
            description=f"""
            Create website content based on:
            {expanded_idea}
            
            Requirements:
            1. Engaging headlines
            2. Clear call-to-actions
            3. SEO-optimized content
            4. Consistent tone
            5. Mobile-friendly formatting
            6. Accessibility compliance
            
            Output directory: {self.output_dir}
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

    def __create_agents(self):
        """Initialize the agent team"""
        toolkit = FileManagementToolkit(
            root_dir=self.output_dir,
            selected_tools=["read_file", "list_directory", "write_file"]
        )

        self.idea_analyst = Agent(
            role="Senior Idea Analyst",
            goal="Analyze and expand website ideas into comprehensive plans",
            backstory="Expert in digital strategy and user experience design",
            verbose=True,
            llm=self.llm,
            tools=toolkit.get_tools()
        )

        self.communications_strategist = Agent(
            role="Senior Communications Strategist",
            goal="Refine website plans into effective communication strategies",
            backstory="Specialist in digital communications and content strategy",
            verbose=True,
            llm=self.llm,
            tools=toolkit.get_tools()
        )

        self.web_developer = Agent(
            role="Senior Web Developer",
            goal="Create modern, responsive websites using Next.js and Shadcn UI",
            backstory="Full-stack developer specializing in modern web technologies",
            verbose=True,
            llm=self.llm,
            tools=toolkit.get_tools()
        )

        self.content_editor = Agent(
            role="Senior Content Editor",
            goal="Create engaging, SEO-optimized website content",
            backstory="Expert in digital content creation and optimization",
            verbose=True,
            llm=self.llm,
            tools=toolkit.get_tools()
        )

    def __log_conversation(self, crew):
        """Log the conversation history"""
        for task in crew.tasks:
            for message in task.messages:
                self.conversation_log.append({
                    'agent': message.agent.name,
                    'role': message.agent.role,
                    'timestamp': datetime.utcnow().isoformat(),
                    'message': message.content
                })
