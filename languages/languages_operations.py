"""
This module provides a function to translate text from English to a 
specified target language using GoogleTranslator.
"""
from deep_translator import GoogleTranslator

def translate(text, target_language):
    """
    Translates the given text into the specified target language using GoogleTranslator.
    
    Parameters:
    - text (str): The text to translate.
    - target_language (str): The target language code (e.g., 'en', 'fr').
    
    Returns:
    - str: The translated text.
    """
    try:
        # Do not translate if the target language is English
        if target_language.lower() == "en":
            return text

        # Perform the translation using Google Translator
        translated_text = GoogleTranslator(source='en', target=target_language).translate(text)
        return translated_text if translated_text else text

    except (ConnectionError, ValueError) as e:
        # Print error message and return the original text if translation fails
        print(f"Translation failed with error: {e}")
        return text
