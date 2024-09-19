"""
This module contains the API routes for the Flask application.
Logging is handled within this file, while utility functions are imported.
"""
import traceback
from datetime import datetime, timedelta
from flask import jsonify, make_response, request
from app import app
from app.news_service import get_ai_news, summarize_news
from languages.languages_operations import translate
from config.cache_config import cache  # Import the cache instance

@app.route('/health', methods=['GET'])
@cache.cached(timeout=60)  # Cache this route for 60 seconds
def health_check():
    """
    Health check endpoint to verify if the API is running.
    ---
    summary: Health Check
    description: |
      This endpoint can be used to verify that the API is up and running. 
      It returns a status message indicating the health of the API.

    responses:
      200:
        description: API is running successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: The status of the API.
                  example: "OK"
                message:
                  type: string
                  description: A message confirming the API is running.
                  example: "API is running."
    """
    app.logger.info("Health check endpoint called.")
    return jsonify({"status": "OK", "message": "API is running."}), 200

@app.route('/daily_news_summary', methods=['POST'])
@cache.cached(timeout=300, key_prefix="daily_news_summary")  # Cache this route for 300 seconds
def daily_news_summary():
    """
    Fetch the latest AI-related news from today and generate a summary.
    ---
    summary: Get today's AI news summary
    description: |
      Fetches the latest AI-related news articles from today and summarizes 
      them using a Hugging Face model. The summary provides a concise overview 
      of the most important AI news from today.

    parameters:
      - in: body
        name: body
        required: true
        description: Request payload to specify the response language.
        schema:
          type: object
          properties:
            language:
              type: string
              description: Language code for the response (e.g., 'en', 'fr', 'tr').
              example: "en"

    responses:
      200:
        description: Successfully returned the AI news summary for today.
        content:
          application/json:
            schema:
              type: object
              properties:
                summary:
                  type: string
                  description: The summary of today's AI news.
                  example: "Here's a summary of today's AI news..."
      400:
        description: Bad Request - No AI news articles available today.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating no news available.
                  example: "No AI news articles available today."
      500:
        description: Internal server error during news summarization.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating an unexpected error.
                  example: "Internal Server Error: An unexpected error occurred."
    """
    app.logger.info("Received request for today's AI news summary.")

    try:
        # Extract the request data and get the language parameter
        data = request.json
        language = data.get('language', 'en')  # Default to English if no language specified

        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")
        app.logger.info(f"Fetching AI-related news articles for today: {today}.")

        # Fetch AI-related news for today
        ai_news = get_ai_news(date=today)

        if not ai_news:
            app.logger.warning(
                "No AI news articles found for today. "
                "Returning a message indicating no news available."
            )
            return jsonify({"error": "No AI news articles available today."}), 400

        # Summarize the news
        app.logger.info(
            f"Fetched {len(ai_news)} AI news articles for today. Proceeding to summarize."
        )
        summary = summarize_news(ai_news)

        if not summary:
            app.logger.warning(
                "Summary generation failed. The summarization returned an empty result."
            )
            return jsonify(
                {"error": "Failed to generate a summary from today's news articles."}
            ), 400

        # Translate the summary if necessary
        translated_summary = translate(summary, language)

        # Return summary as plain text with proper new lines
        app.logger.info("AI news summary generated successfully. Returning the result.")
        response = make_response(translated_summary, 200)
        response.mimetype = "text/plain"
        return response

    except KeyError as ke:
        app.logger.error(f"KeyError occurred: {str(ke)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Missing or invalid key - {str(ke)}"}), 400
    except ValueError as ve:
        app.logger.error(f"ValueError occurred: {str(ve)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Invalid data format - {str(ve)}"}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/weekly_news_summary', methods=['POST'])
@cache.cached(timeout=300, key_prefix="weekly_news_summary")  # Cache this route for 300 seconds
def weekly_news_summary():
    """
    Fetch the latest AI-related news from the last week and generate a summary.
    ---
    summary: Get last week's AI news summary
    description: |
      Fetches the latest AI-related news articles from the last week and 
      summarizes them using a Hugging Face model. This summary provides an 
      overview of the key AI developments over the past week.

    parameters:
      - in: body
        name: body
        required: true
        description: Request payload to specify the response language.
        schema:
          type: object
          properties:
            language:
              type: string
              description: Language code for the response (e.g., 'en', 'fr', 'tr').
              example: "en"

    responses:
      200:
        description: Successfully returned the AI news summary for the last week.
        content:
          application/json:
            schema:
              type: object
              properties:
                summary:
                  type: string
                  description: The summary of the last week's AI news.
                  example: "Here's a summary of the last week's AI news..."
      400:
        description: Bad Request - Failed to fetch news articles.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating failure to fetch news.
                  example: "Bad Request: Failed to fetch news articles."
      500:
        description: Internal server error during news summarization.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating an unexpected error.
                  example: "Internal Server Error: An unexpected error occurred."
    """
    app.logger.info("Received request for last week's AI news summary.")

    try:
        # Extract the request data and get the language parameter
        data = request.json
        language = data.get('language', 'en')  # Default to English if no language specified

        # Calculate the date one week ago
        last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        app.logger.info(f"Fetching AI-related news articles starting from {last_week}.")

        # Fetch AI-related news from the last week
        ai_news = get_ai_news(date=last_week)

        if not ai_news:
            app.logger.warning(
                "No AI news articles fetched for the last week. "
                "The response was empty."
            )
            return jsonify({"error": "No AI news articles available to summarize."}), 400

        # Summarize the news
        app.logger.info(
            f"Fetched {len(ai_news)} AI news articles from the last week. Proceeding to summarize."
        )
        summary = summarize_news(ai_news)

        if not summary:
            app.logger.warning(
                "Summary generation failed. The summarization returned an empty result."
            )
            return jsonify({"error": "Failed to generate a summary from the news articles."}), 400

        # Translate the summary if necessary
        translated_summary = translate(summary, language)

        # Return summary as plain text with proper new lines
        app.logger.info("AI news summary generated successfully. Returning the result.")
        response = make_response(translated_summary, 200)
        response.mimetype = "text/plain"
        return response

    except KeyError as ke:
        app.logger.error(f"KeyError occurred: {str(ke)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Missing or invalid key - {str(ke)}"}), 400
    except ValueError as ve:
        app.logger.error(f"ValueError occurred: {str(ve)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Invalid data format - {str(ve)}"}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/monthly_news_summary', methods=['POST'])
@cache.cached(timeout=300, key_prefix="monthly_news_summary")  # Cache this route for 300 seconds
def monthly_news_summary():
    """
    Fetch the latest AI-related news from the last month and generate a summary.
    ---
    summary: Get last month's AI news summary
    description: |
      Fetches the latest AI-related news articles from the last month and 
      summarizes them using a Hugging Face model. The summary provides an 
      overview of the significant AI news from the past month.

    parameters:
      - in: body
        name: body
        required: true
        description: Request payload to specify the response language.
        schema:
          type: object
          properties:
            language:
              type: string
              description: Language code for the response (e.g., 'en', 'fr', 'tr').
              example: "en"

    responses:
      200:
        description: Successfully returned the AI news summary for the last month.
        content:
          application/json:
            schema:
              type: object
              properties:
                summary:
                  type: string
                  description: The summary of the last month's AI news.
                  example: "Here's a summary of the last month's AI news..."
      400:
        description: Bad Request - Failed to fetch news articles.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating failure to fetch news.
                  example: "Bad Request: Failed to fetch news articles."
      500:
        description: Internal server error during news summarization.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message indicating an unexpected error.
                  example: "Internal Server Error: An unexpected error occurred."
    """
    app.logger.info("Received request for last month's AI news summary.")

    try:
        # Extract the request data and get the language parameter
        data = request.json
        language = data.get('language', 'en')  # Default to English if no language specified

        # Calculate the date 30 days ago
        last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        app.logger.info(f"Fetching AI-related news articles starting from {last_month}.")

        # Fetch AI-related news from the last month
        ai_news = get_ai_news(date=last_month)

        if not ai_news:
            app.logger.warning(
                "No AI news articles fetched for the last month. The response was empty."
            )
            return jsonify({"error": "No AI news articles available to summarize."}), 400

        # Summarize the news
        app.logger.info(
            f"Fetched {len(ai_news)} AI news articles from the last month. Proceeding to summarize."
        )
        summary = summarize_news(ai_news)

        if not summary:
            app.logger.warning(
                "Summary generation failed. The summarization returned an empty result."
            )
            return jsonify({"error": "Failed to generate a summary from the news articles."}), 400

        # Translate the summary if necessary
        translated_summary = translate(summary, language)

        # Return summary as plain text with proper new lines
        app.logger.info("AI news summary generated successfully. Returning the result.")
        response = make_response(translated_summary, 200)
        response.mimetype = "text/plain"
        return response

    except KeyError as ke:
        app.logger.error(f"KeyError occurred: {str(ke)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Missing or invalid key - {str(ke)}"}), 400
    except ValueError as ve:
        app.logger.error(f"ValueError occurred: {str(ve)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Bad Request: Invalid data format - {str(ve)}"}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        app.logger.debug(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
