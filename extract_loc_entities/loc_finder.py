# detects the language of a given tweet

from langdetect import detect

import spacy
nlp = spacy.load('en_core_web_lg')

from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = AutoTokenizer.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
model = AutoModelForTokenClassification.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
clf = pipeline("ner", model=model, tokenizer=tokenizer)

# detects the language
def detect_lang(tweet):
    return (detect(tweet))

# returns a list of entities in the sentence
def give_loc_ents(tweet, lang):   
    return_list = []
    if lang == "en":
        doc = nlp(tweet)
        for ent in doc.ents:
            if ent.label_ == "FAC" or ent.label_ == "ORG" or ent.label_ == "GPE" or ent.label_ == "LOC":
                return_list.append(ent.text)

        return return_list

    elif lang == "tr":
        tweet = tweet.replace("'", " ")
        word_list = tweet.split(" ")
        nlp = clf(tweet)
        for i in range(0, len(nlp)):
            if nlp[i]["entity"] == "B-ORGANIZATION":
                add = ""           
                word = nlp[i]["word"].replace("#", "")
                for item in word_list:
                    if word in item:
                        if item not in return_list:
                            add += (item + " ")
                if i < (len(nlp)-1):
                    d = i+1
                    while nlp[d]["entity"] == "I-ORGANIZATION":
                        word = nlp[d]["word"].replace("#", "")
                        for item in word_list:
                            if word in item:
                                if item not in return_list:
                                    add += (item + " ")
                        if d < (len(nlp)-1):
                            d = d+1
                        else:
                            break
                return_list.append(add[:-1])

            elif nlp[i]["entity"] == "B-LOCATION":
                add = ""           
                word = nlp[i]["word"].replace("#", "")
                for item in word_list:
                    if word in item:
                        if item not in return_list:
                            add += (item + " ")
                if i < (len(nlp)-1):
                    d = i+1
                    while nlp[d]["entity"] == "I-LOCATION":
                        word = nlp[d]["word"].replace("#", "")
                        for item in word_list:
                            if word in item:
                                if item not in return_list:
                                    add += (item + " ")
                        if d < (len(nlp)-1):
                            d = d+1
                        else:
                            break
                return_list.append(add[:-1])

        return return_list
    
