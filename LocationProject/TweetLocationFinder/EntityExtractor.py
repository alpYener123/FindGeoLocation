# This class is for finding location entities in a given tweet

from unidecode import unidecode
from langdetect import detect
import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


'''
USAGE:
1) Get the language
2) get the loc_ents as a list
3) use gather.ilce_dict etc and every string in the list with is_substring_in_nested_dict function
4) use find_city function
5) voila
'''

class EntityExtractor:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.tokenizer = AutoTokenizer.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
        self.model = AutoModelForTokenClassification.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
        self.clf = pipeline("ner", model=self.model, tokenizer=self.tokenizer)


    # detects the language
    @staticmethod
    def detect_lang(tweet):
        return (detect(tweet))

    # returns a list of entities in the sentence
    def give_loc_ents(self, tweet, lang):

        return_list = []
        if lang == "en":
            doc = self.nlp(tweet)
            for ent in doc.ents:
                if ent.label_ == "FAC" or ent.label_ == "ORG" or ent.label_ == "GPE" or ent.label_ == "LOC":
                    return_list.append(ent.text)

            return return_list

        elif lang == "tr":
            
            tweet = tweet.replace("'", " ")
            word_list = tweet.split(" ")
            nlp = self.clf(tweet)
            for i in range(0, len(nlp)):
                '''if nlp[i]["entity"] == "B-ORGANIZATION":
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
                                    if item not in return_list and item not in add:
                                        add += (item + " ")
                            if d < (len(nlp)-1):
                                d = d+1
                            else:
                                break
                    return_list.append(add[:-1])'''

                if nlp[i]["entity"] == "B-LOCATION":
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
                                    if item not in return_list and item not in add:
                                        add += (item + " ")
                            if d < (len(nlp)-1):
                                d = d+1
                            else:
                                break
                    add = add[:-1]
                    add = unidecode(add.strip())
                    add = add.lower()
                    return_list.append(add)

            return return_list



# May be deleted
def is_substring_in_nested_dict(dct, target_string, check=False):
    for key, value in dct.items():
        if isinstance(value, dict):
            result = is_substring_in_nested_dict(value, target_string, check=True)
            if result is not False:
                return result
        elif isinstance(key, str) and key in target_string and check:
            return key
    return False