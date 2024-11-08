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
