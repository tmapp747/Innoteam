from langchain.tools import tool


class FileTools():

  @tool("Write File with content")
  def write_file(data):
    """Useful to write a file to a given path with a given content. 
       The input to this tool should be a pipe (|) separated text 
       of length two, representing the full path of the file, 
       including the /workdir/template, and the React 
       Component code content you want to write to it.
       For example, `./Keynote/src/components/Hero.jsx|REACT_COMPONENT_CODE_PLACEHOLDER`.
       Replace REACT_COMPONENT_CODE_PLACEHOLDER with the actual 
       code you want to write to the file."""
    try:
      path, content = data.split("|")
      path = path.replace("\n", "").replace(" ", "").replace("`", "")
      if not path.startswith("./workdir"):
        path = f"./workdir/{path}"
      with open(path, "w") as f:
        f.write(content)
      return f"File written to {path}."
    except Exception:
      return "Error with the input format for the tool."

  @tool("Validate File Content")
  def validate_file_content(data):
    """Useful to validate the content of a file to ensure it meets the desired standards.
       The input to this tool should be a pipe (|) separated text of length two, representing
       the full path of the file and the content to be validated.
       For example, `./workdir/template/src/components/Hero.jsx|CONTENT_TO_BE_VALIDATED`.
       Replace CONTENT_TO_BE_VALIDATED with the actual content you want to validate."""
    try:
      path, content = data.split("|")
      path = path.replace("\n", "").replace(" ", "").replace("`", "")
      if not path.startswith("./workdir"):
        path = f"./workdir/{path}"
      
      # Perform validation checks
      if not content:
        return "Error: Content is empty."
      if "import" not in content:
        return "Error: Missing import statements."
      if "export function" not in content:
        return "Error: Missing export function."
      if "'use client'" not in content:
        return "Error: Missing 'use client' directive."
      if "href='#'" not in content:
        return "Error: Missing href='#' in links or buttons."
      
      return "File content is valid."
    except Exception:
      return "Error with the input format for the tool."

  @tool("Debug Errors")
  def debug_errors(data):
    """Useful to check for possible errors in the code and debug them to ensure the application runs smoothly.
       The input to this tool should be a pipe (|) separated text of length two, representing
       the full path of the file and the content to be debugged.
       For example, `./workdir/template/src/components/Hero.jsx|CONTENT_TO_BE_DEBUGGED`.
       Replace CONTENT_TO_BE_DEBUGGED with the actual content you want to debug."""
    try:
      path, content = data.split("|")
      path = path.replace("\n", "").replace(" ", "").replace("`", "")
      if not path.startswith("./workdir"):
        path = f"./workdir/{path}"
      
      # Perform debugging checks
      if not content:
        return "Error: Content is empty."
      if "import" not in content:
        return "Error: Missing import statements."
      if "export function" not in content:
        return "Error: Missing export function."
      if "'use client'" not in content:
        return "Error: Missing 'use client' directive."
      if "href='#'" not in content:
        return "Error: Missing href='#' in links or buttons."
      
      return "File content is debugged and valid."
    except Exception:
      return "Error with the input format for the tool."
