


# **Web Search and Summarization Service**

## **Overview**
This project is a Flask-based web service that performs the following tasks:
1. Accepts a list of search terms via an API endpoint.
2. Retrieves the top search results using Google Search.
3. Scrapes the content from the resulting websites.
4. Summarizes the scraped content using the Gemini API through LangChain integration.
5. Returns the structured data in JSON format.

## **Features**
- **Dynamic Web Search**: Retrieves the top search results for any given search terms.
- **Content Scraping**: Extracts titles and main body content from websites.
- **Summarization**: Uses the Gemini API via LangChain to summarize scraped content.
- **JSON Output**: Returns results in an easy-to-consume JSON structure.

---

## **Technologies Used**
- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Web Search**: [Google Search Python Library](https://pypi.org/project/googlesearch-python/)
- **Web Scraping**: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- **Language Model Integration**: [LangChain](https://www.langchain.com/) with Gemini API
- **API Communication**: [Requests](https://pypi.org/project/requests/)

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### **2. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the root directory with the following content:
```
GEMINI_API_KEY=your_gemini_api_key
```

### **5. Run the Application**
```bash
python app.py
```
The application will run on `http://localhost:5000`.

---

## **API Usage**

### **Endpoint**: `/search`

**Method**: POST  
**Content-Type**: `application/json`  

**Request Body Example**:
```json
{
    "search_terms": ["Python tutorial", "Machine learning basics"],
    "num_results": 5
}
```

**Response Example**:
```json
[
    {
        "search_term": "Python tutorial",
        "results": [
            {
                "url": "https://example.com/python",
                "title": "Learn Python",
                "body_content": "Python is a versatile programming language...",
                "summary": "Python is a versatile and beginner-friendly programming language."
            }
        ]
    }
]
```

---

## **File Structure**
```
├── app.py                # Flask application
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
├── .env                  # Environment variables (not committed)
└── venv/                 # Virtual environment (ignored by Git)
```

---

## **Contributing**
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.
