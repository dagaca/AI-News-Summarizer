"""
This module provides functions to fetch AI-related news from NewsAPI 
and summarize them using Hugging Face models.
"""
import os
import requests
from huggingface_hub import InferenceClient

# Function to fetch AI-related news from NewsAPI
def get_ai_news(date):
    """
    Fetch the latest AI-related news articles using NewsAPI.
    Args:
        date (str): Date for filtering news articles in YYYY-MM-DD format.
    Returns:
        list: A list of the last 10 news articles with title and description, or None on failure.
    """
    api_key = os.getenv("NEWS_API_KEY")

    url = (
        "https://newsapi.org/v2/everything?q=artificial+intelligence"
        f"&from={date}"  # Fetch articles starting from the provided date
        "&sortBy=publishedAt"
        "&pageSize=100"  # Fetch up to 100 articles to ensure enough data for summarization
        f"&apiKey={api_key}"
    )

    response = requests.get(url, timeout=60)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        # Return only the last 10 articles
        return [f"{article['title']}: {article['description']}" for article in articles[-10:]]
    return None

# Function to create a professional summarization prompt
def create_prompt(news_articles):
    """
    Creates a refined summarization prompt for AI-related news.
    Args:
        news_articles (list): A list of AI-related news articles.
    Returns:
        str: A polished prompt for summarization.
    """
    prompt = (
        "Please provide a clear and concise summary of the following "
        "100 AI-related news articles. "
        "Ensure the summary highlights the most important information, "
        "is coherent, and flows naturally. "
        "The output should be structured in a professional manner, "
        "with attention to readability and clarity, "
        "making it suitable for inclusion in reports or articles. "
        "Focus on delivering an insightful overview "
        "that avoids unnecessary repetition, while maintaining "
        "a smooth narrative throughout. "
        "Ensure that no special characters (such as '\\n', '\\t', or other symbols) "
        "are included in the output."
    )
    return f"{prompt} {' '.join(news_articles)}"

# Function to summarize news using Hugging Face model
def summarize_news(news_articles):
    """
    Summarizes AI-related news articles using Hugging Face's Inference API.
    Args:
        news_articles (list): A list of AI-related news articles.
    Returns:
        str: A clean, structured summary of the news articles.
    """
    client = InferenceClient(token=os.getenv("HF_API_TOKEN"))
    prompt = create_prompt(news_articles)

    # Create the message structure for the API call
    messages = [{"role": "user", "content": prompt}]

    # Collect the summary from the model
    summary = ""
    for message in client.chat_completion(messages=messages, max_tokens=2000, stream=True):
        summary += message.choices[0].delta.content
    return summary.strip()
