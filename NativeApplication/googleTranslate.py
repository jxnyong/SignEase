# pip install --upgrade googletrans==4.0.0-rc1
# pip install --upgrade httpcore

#this is specifically for googleTranslate, capability of translating romanji/romanized text.
#dependency issue with httpx > mongodb
from googletrans import Translator
import json, re

#language code: Zh-CN, En, Ja
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

def googleTranslate(text):
    outLANG = getOutLang()
    translator = Translator()
    translated_text = translator.translate(text, src=inLANG, dest=outLANG)
    return translated_text.text

def extract_complete_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # regular expression to split the text into sentences.
    sentences = re.split(r'(?<=[.!?。])\s+', text)
    complete_sentences = []

    for sentence in sentences:
        if re.search(r'[.!?。]$', sentence):
            # sentence ends with punctuation, consider it a complete sentence.
            complete_sentences.append(sentence)

    return complete_sentences

# for LiveTranslation
with open('translatedText.txt', 'w', encoding='utf-8' ) as f:
    target_language = getOutLang() #language to translate to
    with open('transcript.txt', 'r', encoding='utf-8') as t:
        file_path = "transcript.txt"
        complete_sentences = extract_complete_sentences(file_path)
        separator = ' '  #  separator between the elements of the list
        strCompleteSentences = separator.join(complete_sentences)
    f.write(googleTranslate(strCompleteSentences))





#NOT USED
# import argparse
#chinese: dest='zh-CN'
#japanese: dest='ja'
#english: dest='en'

# if __name__ == "__main__":
#     translator = Translator()
#     # Import the library
#     # Create the parser
#     parser = argparse.ArgumentParser()
#     # Add an argument
#     parser.add_argument('phrase', type=str)
#     parser.add_argument('dest', type=str)
#     parser.add_argument('-s','--src', type=str, nargs='?')
#     parser.add_argument("-dsf","--disable_save_file", action="store_true", help="Enable verbose mode")
#     parser.add_argument("-file","--file_name", type=str, nargs='?')

#     # Parse the argument
#     args = parser.parse_args()
#     translated_text = translator.translate(args.phrase, src=args.src if args.src else 'En', dest=args.dest).text
#     if not args.disable_save_file:
#         with open(file=args.file_name if args.file_name else "translatedText.txt", mode="w", encoding='utf-8') as file:
#             file.write(translated_text)
#     print(translated_text)

# #demo: python googleTranslate.py "let's start the meeting" Zh-CN -dsf
