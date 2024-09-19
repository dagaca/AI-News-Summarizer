# AI-News-Summarizer

The AI News Summary API is a Flask-based application that fetches the latest AI-related news articles from NewsAPI, generates concise summaries using Hugging Face models, and provides these summaries in various languages. This API is designed to help users stay updated on the latest developments in artificial intelligence by providing summarized news articles from today, the last week, or the last month.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Daily News Summary](#daily-news-summary)
  - [Weekly News Summary](#weekly-news-summary)
  - [Monthly News Summary](#monthly-news-summary)
- [Caching](#caching)
- [Error Handling](#error-handling)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features
- **Fetch AI News**: Retrieves the latest AI-related news articles from NewsAPI.
- **Summarize News**: Uses Hugging Face models to generate concise and readable summaries of news articles.
- **Multi-language Support**: Summaries can be translated into different languages based on user input.
- **Caching**: Implements caching to optimize performance and reduce redundant processing.
- **Logging**: Detailed logging to monitor API requests, responses, and errors.

## How It Works
1. **Fetch News Articles**: The application uses NewsAPI to fetch AI-related news articles based on the specified date range (today, last week, last month).
2. **Generate Summaries**: Summaries are generated using Hugging Face models, providing a concise overview of the most significant AI news.
3. **Translate Summaries**: The summaries can be translated into different languages using the integrated translation functionality.
4. **Caching**: Responses are cached to improve performance, minimizing redundant requests to the NewsAPI and Hugging Face models.

### NewsAPI Integration
The API fetches AI-related news articles using [NewsAPI](https://newsapi.org/), a service that provides access to various news sources and articles worldwide. The `get_ai_news` function constructs a request to NewsAPI, using a specific query to filter articles related to artificial intelligence.

**Key Details of NewsAPI Integration:**
- **Endpoint Used**: `https://newsapi.org/v2/everything`
- **Query Parameters**:
  - `q=artificial+intelligence`: Searches for articles containing the phrase "artificial intelligence."
  - `from`: Filters articles starting from a specified date in YYYY-MM-DD format.
  - `sortBy=publishedAt`: Sorts articles by their publication date.
  - `pageSize=100`: Fetches up to 100 articles to ensure enough data for summarization.
  - `apiKey`: Your unique API key for authenticating requests to NewsAPI.

## Getting Started
Follow these instructions to set up and run the API on your local machine.

### Prerequisites
- Python 3.8+
- Flask
- Flask-Caching
- Hugging Face API
- NewsAPI Key
- Postman (optional for testing)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
   
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
## Configuration

1. **Environment Variables:** Create a .env file in the root directory of the project and set up the following variables:

  ```bash
  FLASK_ENV=development
  NEWS_API_KEY=<your-news-api-key>
  HF_API_TOKEN=<your-hugging-face-api-token>
  LOG_DIR=logs
  ```

- Replace <your-news-api-key> with your NewsAPI key.
- Replace <your-hugging-face-api-token> with your Hugging Face API token.

2. **Cache Configuration:** The cache is configured in the cache_config.py file with a default timeout of 300 seconds. Adjust the configuration as needed for your environment.

## Running the Application
To start the Flask application, run:

  ```bash
  flask run
  ```

The application will start on **http://localhost:5000** by default.

## API Endpoints with Swagger Results
To provide a more interactive understanding of how each endpoint works, here are screenshots of the Swagger UI showcasing the requests and responses for each endpoint.

**Health Check**
Endpoint: /health
Method: GET
Description: Checks if the API is running.

Swagger Request and Response Screenshot:


**Daily News Summary**
Endpoint: /daily_news_summary
Method: POST
Description: Fetches and summarizes the latest AI-related news from today.
Request Body:

  ```bash
  {
    "language": "en"  // Specify the language code, e.g., 'en' for English, 'fr' for French
  }
  ```

Swagger Request and Response Screenshot:


**Weekly News Summary**
Endpoint: /weekly_news_summary
Method: POST
Description: Fetches and summarizes AI-related news from the last week.
Request Body:

  ```bash
  {
    "language": "en"  // Specify the language code, e.g., 'en' for English, 'fr' for French
  }
  ```

Swagger Request and Response Screenshot:


**Monthly News Summary**
Endpoint: /monthly_news_summary
Method: POST
Description: Fetches and summarizes AI-related news from the last month.
Request Body:

  ```bash
  {
    "language": "en"  // Specify the language code, e.g., 'en' for English, 'fr' for French
  }
  ```

Swagger Request and Response Screenshot:


## Caching
Caching is implemented using Flask-Caching with a simple backend by default. Responses are cached for 5 minutes to improve performance and reduce repeated computations.
Cache configuration is adjustable in the **cache_config.py** file.
Example of caching usage in routes:
  ```bash
  @cache.cached(timeout=300, key_prefix="daily_news_summary")
  def daily_news_summary():
      # Function implementation
  ```


## Error Handling
The API handles errors gracefully and provides clear messages:

**400 Bad Request:** Returned when input data is missing or invalid.
**500 Internal Server Error:** Returned when an unexpected error occurs during processing.


## Technologies Used
Flask: Web framework used for creating the API.
Flask-Caching: For caching API responses to enhance performance.
Hugging Face API: Used for generating AI summaries of news articles.
NewsAPI: Source of AI-related news articles.
Postman: Optional tool for testing and interacting with the API.


## License
This project is licensed under the MIT License, which permits use, distribution, and modification with attribution.
