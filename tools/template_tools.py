import json
import shutil
from pathlib import Path

from langchain.tools import tool


class TemplateTools():

  @tool("Learn landing page options")
  def learn_landing_page_options(input):
    """Learn the templates at your disposal"""
    templates = json.load(open("config/templates.json"))
    return json.dumps(templates, indent=2)

  @tool("Copy landing page template to project folder")
  def copy_landing_page_template_to_project_folder(landing_page_template):
    """Copy a landing page template to your project 
    folder so you can start modifying it, it expects 
    a landing page template folder as input"""
    source_path = Path(f"templates/{landing_page_template}")
    destination_path = Path(f"workdir/{landing_page_template}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_path, destination_path)
    return f"Template copied to {landing_page_template} and ready to be modified, main files should be under ./{landing_page_template}/src/components, you should focus on those."

  @tool("Validate Template Integration")
  def validate_template_integration(data):
    """Useful to validate the integration of the template to ensure it is properly copied and ready for modification.
       The input to this tool should be the name of the landing page template.
       For example, `Keynote`."""
    try:
      template_name = data.strip()
      source_path = Path(f"templates/{template_name}")
      destination_path = Path(f"workdir/{template_name}")

      if not source_path.exists():
        return f"Error: Source template {template_name} does not exist."
      if not destination_path.exists():
        return f"Error: Destination path {template_name} does not exist."

      return f"Template {template_name} is properly integrated and ready for modification."
    except Exception:
      return "Error with the input format for the tool."
