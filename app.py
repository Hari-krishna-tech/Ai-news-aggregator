from flask import Flask, request, jsonify
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',  # Choose the appropriate model
    temperature=0.7,     # Adjust creativity level as needed
    api_key=GEMINI_API_KEY
)


# Initialize Flask app
app = Flask(__name__)

# Set your Gemini API key
GEMINI_API_KEY = "your_gemini_api_key"

def create_json_from_ai_response(ai_response):
    """
    Create a JSON object from the AI response.
    """
    ai_response = ai_response.strip("```json\n").strip("```")
    try:
        response = json.loads(ai_response)
        return response
    except Exception as e:
        return {"error": f"Error parsing AI response: {str(e)}"}

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
        body_content = body_content  # Limit to first 2000 characters for readability

        return title, body_content
    except Exception as e:
        return "Error", f"Error scraping {url}: {str(e)}"

def generate_overall_summary_with_gemini(term_results):
    """
    Use the Gemini model via LangChain to generate a summary of the given content.
    """
    data = ""
    for d in term_results:
        data += d["body"]
        data += "\n"

    try:
        prompt = f"Summarize the following content and provide a detailed summary in 1000 words: (just summary with point don't need to give pretext only list of summaries ) formate it in json should not have any new line in it just json(details and headline only)\n\n{data}"
        response = llm.invoke(prompt)

        return response.content.strip()
    except Exception as e:
        print(f"Error generating summary with Gemini: {e}")
        return "Error generating summary"

def create_use_full_search_term(term):
    """
    Use the Gemini model via LangChain to generate a summary of the given content.
    """
    try:
        prompt = f"Give list the search terms we can use in google the following term to find the most recent news(trending news) give result in the form of search term,search term,search term and nothing else give atleast 5:\n\n{term}"
        response = llm.invoke(prompt)
        terms = response.content.strip().split(",")
        print(term ,terms)
        return terms
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
            # Perform a web search
            terms = create_use_full_search_term(term)
            websites = []
            for llm_term in terms:
                
                websites += perform_web_search(llm_term, num_results=2)
            term_results = []

            if isinstance(websites, dict) and "error" in websites:
                term_results.append({"error": websites["error"]})
            else:
                for website in websites:
                    title, body_content = scrape_website_content(website)


                    term_results.append({
                        "url": website,
                        "title": title,
						"body":body_content, 
                        
                    })
            termSummary = generate_overall_summary_with_gemini(term_results)	
            """
            
            """
            # convert termsummary to json format
            results.append({"search_term": term, "results": create_json_from_ai_response(termSummary)})
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
