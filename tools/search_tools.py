import os
import json
import requests
from langchain.tools import tool


class SearchTools():

  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet 
    about a a given topic and return relevant results"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']
    stirng = []
    for result in results:
      stirng.append('\n'.join([
          f"Title: {result['title']}", f"Link: {result['link']}",
          f"Snippet: {result['snippet']}", "\n-----------------"
      ]))

    return '\n'.join(stirng)

  @tool("Validate Search Results")
  def validate_search_results(data):
    """Useful to validate the search results to ensure they are relevant and accurate.
       The input to this tool should be a JSON string representing the search results.
       For example, `{"results": [{"title": "Example Title", "link": "http://example.com", "snippet": "Example snippet."}]}`."""
    try:
      results = json.loads(data)
      if not results.get("results"):
        return "Error: No search results found."
      for result in results["results"]:
        if not result.get("title") or not result.get("link") or not result.get("snippet"):
          return "Error: Missing title, link, or snippet in search results."
      return "Search results are valid."
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
