from tkinter import N
from googletrans import Translator


async def detect(text:str):
    """
    Detects the language of the given text.

    Args:
        text (str): The text whose language needs to be detected.

    Returns:
        str: The detected language code (e.g., 'en' for English).
    """

    async with Translator() as translator:
        result = await translator.detect(text)
        return result.lang


async def translate_text(text:str, src:str=None):
    """Translate text from one language to another.

    Args:
        text (str): The text to translate.
        src (str): The source language to translate from.

    Returns:
        str: The translated text.
        tuple: The translated text and the target language if src is None.
    """
    
    if src:
        async with Translator() as translator:
            result = await translator.translate(text, dest=src)
            return result.text
    else:
        async with Translator() as translator:
            result = await translator.translate(text)
            return result.text, result.src

        
