import json
import os
import shutil
from textwrap import dedent

from crewai import Agent, Crew, Task
from langchain.agents.agent_toolkits import FileManagementToolkit
from tasks import TaskPrompts

from tools.browser_tools import BrowserTools
from tools.file_tools import FileTools
from tools.search_tools import SearchTools
from tools.template_tools import TemplateTools

from flask import Flask, render_template, request, jsonify

# Add imports for Claude 3.5, Sonnet, and Deep Seek models
from langchain.llms import Claude, Sonnet, DeepSeek

app = Flask(__name__)

class LandingPageCrew():
  def __init__(self, idea, llm=None):
    self.agents_config = json.loads(open("config/agents.json", "r").read())
    self.idea = idea
    self.llm = llm
    self.__create_agents()

  def run(self):
    expanded_idea = self.__expand_idea()
    components = self.__choose_template(expanded_idea)
    self.__update_components(components, expanded_idea)

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
    return expanded_idea

  def __choose_template(self, expanded_idea):
    choose_tempalte_taks = Task(
        description=TaskPrompts.choose_template().format(
          idea=self.idea
        ),
        agent=self.react_developer
    )
    update_page = Task(
      description=TaskPrompts.update_page().format(
        idea=self.idea
      ),
      agent=self.react_developer
    )
    crew = Crew(
      agents=[self.react_developer],
      tasks=[choose_tempalte_taks, update_page],
      verbose=True
    )
    components = crew.kickoff()
    return components

  def __update_components(self, components, expanded_idea):
    components = components.replace("\n", "").replace(" ",
                                                      "").replace("```", "")
    components = json.loads(components)
    for component in components:
      file_content = open(
        f"./workdir/{component.split('./')[-1]}",
        "r"
      ).read()
      create_content = Task(
        description=TaskPrompts.component_content().format(
          expanded_idea=expanded_idea,
          file_content=file_content,
          component=component
        ),
        agent=self.content_editor_agent
      )
      update_component = Task(
        description=TaskPrompts.update_component().format(
          component=component,
          file_content=file_content
        ),
        agent=self.react_developer
      )
      qa_component = Task(
        description=TaskPrompts.qa_component().format(
          component=component
        ),
        agent=self.react_developer
      )
      crew = Crew(
        agents=[self.content_editor_agent, self.react_developer],
        tasks=[create_content, update_component, qa_component],
        verbose=True
      )
      crew.kickoff()

  def __create_agents(self):
    idea_analyst_config = self.agents_config["senior_idea_analyst"]
    strategist_config = self.agents_config["senior_strategist"]
    developer_config = self.agents_config["senior_react_engineer"]
    editor_config = self.agents_config["senior_content_editor"]

    toolkit = FileManagementToolkit(
      root_dir='workdir',
      selected_tools=["read_file", "list_directory"]
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

    self.react_developer = Agent(
      **developer_config,
      verbose=True,
      llm=self.llm,
      tools=[
          SearchTools.search_internet,
          BrowserTools.scrape_and_summarize_kwebsite,
          TemplateTools.learn_landing_page_options,
          TemplateTools.copy_landing_page_template_to_project_folder,
          FileTools.write_file
      ] + toolkit.get_tools()
    )

    self.content_editor_agent = Agent(
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

    crew = LandingPageCrew(idea, llm)
    crew.run()
    return jsonify({"message": "Landing page generated successfully!"})

if __name__ == "__main__":
  app.run(debug=True)
