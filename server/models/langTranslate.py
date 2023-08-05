from translate import Translator

#translation, perform retrieval of output language constantly
def translate_text(text, outLang, inLang="En"):
    translator = Translator(from_lang=inLang, to_lang=outLang)
    translated_text = translator.translate(text)
    return translated_text
