import asyncio
from playwright.async_api import async_playwright
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

class BrowserTools():
    @staticmethod
    async def _get_page_content(url):
        """Internal method to get page content using playwright"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until='networkidle')
                content = await page.content()
                return content
            finally:
                await browser.close()

    @tool("Scrape website content")
    def scrape_and_summarize_kwebsite(website):
        """Useful to scrape and summarize a website content"""
        try:
            # Get content using playwright
            content = asyncio.run(BrowserTools._get_page_content(website))

            # Process the HTML content
            elements = partition_html(text=content)
            content = "\n\n".join([str(el) for el in elements])

            # Split content into manageable chunks
            chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]

            # Process each chunk
            summaries = []
            for chunk in chunks:
                agent = Agent(
                    role='Principal Researcher',
                    goal='Do amazing researches and summaries based on the content you are working with',
                    backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                    allow_delegation=False
                )

                task = Task(
                    agent=agent,
                    description=f'''
                        Analyze and summarize the content below, make sure to include 
                        the most relevant information in the summary, return only 
                        the summary nothing else.

                        CONTENT
                        ----------
                        {chunk}
                    '''
                )

                summary = task.execute()
                summaries.append(summary)

            # Combine all summaries
            return "\n\n".join(summaries)

        except Exception as e:
            return f"Error scraping website: {str(e)}"
