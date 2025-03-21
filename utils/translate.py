from googletrans import Translator


        
async def translate_text_to_english(text:str):
    """
    Translate given text into English language.

    Args:
        text (str): The text to translate.

    Returns:
        tuple: A tuple containing the translated text and the detected source language.
    """
    async with Translator() as translator:
        result = await translator.translate(text)
        return result.text, result.src
    
    
async def translate_text_to_src(text:str, src:str):
    """
    Translate given text into given source language.

    Args:
        text (str): The text to translate.
        src (str): The source language to translate to.

    Returns:
        str: The translated text.
    """
    async with Translator() as translator:
        result = await translator.translate(text, dest=src)
        return result.text
        

        
