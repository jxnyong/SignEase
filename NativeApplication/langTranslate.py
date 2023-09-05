#this is specifically for translate, does not have capability of translating romanji/romanized text.
#does not have dependency issue with httpx > mongodb
import cv2
from translate import Translator
import json, re

#language code: Zh, En, Ja
#to retrieve default/current settings
with open('langConfig.json', 'r') as f:
    data = json.load(f)
    inLANG:str = data["Setting"]["inputLanguage"]
    outLANG:str = data["Setting"]["outputLanguage"]

#to retrieve the output language
def getOutLang(configFile:str='langConfig.json'):
    with open(configFile, 'r') as f:
        data = json.load(f)
        outLANG:str = data["Setting"]["outputLanguage"]
    return outLANG

def getFONT(configFile:str='langConfig.json'):
    with open(configFile, 'r') as f:
        data = json.load(f)
        outLANG:str = data["Setting"]["outputLanguage"]
        FONT = cv2.FONT_HERSHEY_PLAIN if outLANG == "En" else data["Languages"][outLANG]
    return FONT

#translation, perform retrieval of output language constantly
def translate_text(text):
    outLANG = getOutLang()
    translator = Translator(from_lang=inLANG, to_lang=outLANG)
    translated_text = translator.translate(text)
    return translated_text

#for LiveTranslation
#function to extract complete sentences to be translated (need wait for jaren's NLP)
def extract_complete_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # regular expression to split the text into sentences.
    sentences = re.split(r'(?<=[.!?。])\s+', text)
    complete_sentences = []

    for sentence in sentences:
        if re.search(r'[.!?]$', sentence):
            # sentence ends with punctuation, consider it a complete sentence.
            complete_sentences.append(sentence)

    return complete_sentences

#for testing
#for Subtitling
# with open('translatedSubtitles.txt', 'w', encoding='utf-8' ) as f:
#     target_language = outLANG #language to translate to
#     with open('subtitles.txt', 'r', encoding='utf-8') as t:
#         file_path = "Subtitles.txt"
#         complete_sentences = extract_complete_sentences(file_path)
#         separator = ' '  #  separator between the elements of the list
#         strCompleteSentences = separator.join(complete_sentences)
#     f.write(translate_text(strCompleteSentences))

# for LiveTranslation
with open('translatedText.txt', 'w', encoding='utf-8' ) as f:
    target_language = getOutLang() #language to translate to
    with open('transcript.txt', 'r', encoding='utf-8') as t:
        file_path = "transcript.txt"
        complete_sentences = extract_complete_sentences(file_path)
        separator = ' '  #  separator between the elements of the list
        strCompleteSentences = separator.join(complete_sentences)
    f.write(translate_text(strCompleteSentences))

# if __name__ == '__main__':
#     print(translate_text("hello"))