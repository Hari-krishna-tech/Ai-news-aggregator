from flask import Flask, request, jsonify
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model='gemini-pro',  # Choose the appropriate model
    temperature=0.7,     # Adjust creativity level as needed
    api_key=GEMINI_API_KEY
)


# Initialize Flask app
app = Flask(__name__)

# Set your Gemini API key
GEMINI_API_KEY = "your_gemini_api_key"

def perform_web_search(query, num_results=10):
    """
    Perform a web search and return the top websites.
    """
    try:
        websites = []
        for url in search(query, num_results=num_results):
            websites.append(url)
        return websites
    except Exception as e:
        return {"error": f"Error during web search: {str(e)}"}

def scrape_website_content(url):
    """
    Scrape the title and main body content of a website.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the title
        title = soup.title.string.strip() if soup.title else "No Title"

        # Extract main body content
        paragraphs = soup.find_all('p')
        body_content = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        body_content = body_content[:2000]  # Limit to first 2000 characters for readability

        return title, body_content
    except Exception as e:
        return "Error", f"Error scraping {url}: {str(e)}"

def generate_summary_with_gemini(content):
    """
    Use the Gemini model via LangChain to generate a summary of the given content.
    """
    try:
        prompt = f"Summarize the following content:\n\n{content}"
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"Error generating summary with Gemini: {e}")
        return "Error generating summary"


@app.route('/search', methods=['POST'])
def search_and_summarize():
    """
    Endpoint to perform a web search, scrape content, generate summaries, and return results.
    """
    try:
        # Get the search terms from the request body
        request_data = request.json
        search_terms = request_data.get("search_terms", [])
        num_results = request_data.get("num_results", 10)

        if not search_terms or not isinstance(search_terms, list):
            return jsonify({"error": "Invalid input. Provide a list of search terms."}), 400

        results = []

        for term in search_terms:
            websites = perform_web_search(term, num_results=num_results)
            term_results = []

            if isinstance(websites, dict) and "error" in websites:
                term_results.append({"error": websites["error"]})
            else:
                for website in websites:
                    title, body_content = scrape_website_content(website)

                    if body_content != "Error":
                        summary = generate_summary_with_gemini(body_content)
                    else:
                        summary = "Error"

                    term_results.append({
                        "url": website,
                        "title": title,
                        "body_content": body_content,
                        "summary": summary
                    })

            results.append({"search_term": term, "results": term_results})

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
