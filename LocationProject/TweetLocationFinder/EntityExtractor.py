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

    def __init__(self, tweet):
        self.nlp = spacy.load('en_core_web_lg')
        self.tokenizer = AutoTokenizer.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
        self.model = AutoModelForTokenClassification.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
        self.clf = pipeline("ner", model=self.model, tokenizer=self.tokenizer)
        self.tweet = tweet


    # detects the language
    def detect_lang(self):
        lang = detect(self.tweet)
        print("Language: ", lang)
        return lang

    # returns a list of entities in the sentence
    def give_loc_ents(self, lang):

        return_list = []
        if lang == "en":
            doc = self.nlp(self.tweet)
            for ent in doc.ents:
                if ent.label_ == "FAC" or ent.label_ == "ORG" or ent.label_ == "GPE" or ent.label_ == "LOC":
                    return_list.append(ent.text)

            return return_list

        elif lang == "tr":
            
            tweet = self.tweet.replace("'", " ")
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

    '''def _is_substring_in_nested_dict(self, dct, target_string, check=False, city = ""):
        for key, value in dct.items():
            if isinstance(value, dict):
                result = self._is_substring_in_nested_dict(value, target_string, check=True, city = key)
                if result is not False:
                    return result
            elif isinstance(key, str) and key in target_string and check:
                return city
        return False
    
    def find_cities(self, city_list, ilce_dict, semt_dict, mah_dict, list):
        for item in list:
            if item in city_list:
                print("Entity ", item, " is a city.")
            else:
                ilce = self._is_substring_in_nested_dict(ilce_dict, item)
                if ilce != False:
                    print("Entity ", item, " is in city ", ilce)

                else:
                    semt = self._is_substring_in_nested_dict(semt_dict, item)
                    if semt != False:
                        print("Entity ", item, " is in city ", semt)
                    else:
                        mah = self._is_substring_in_nested_dict(mah_dict, item)
                        if mah != False:
                            print("Entity ", item, " is in city ", mah)
                        else:
                            print("Could not find a corresponding city for ", item)'''


    def _recursive_search(self, sub_dict, st, cities, city=""):
        for key, value in sub_dict.items():
            if isinstance(value, dict):
                cities = self._recursive_search(value, st, cities, key)
            elif key in st and city not in cities:
                cities+=(city+",")
        return cities

    def _find_cities(self, dct, target_string):
        common = ""
        common = self._recursive_search(dct, target_string, common)
        if len(common) > 0:
            common = common[:-1]
            common = common.split(",")
        return common

    def show_cities(self, city_list, idct, sdic, mdic, list):
        ok = False
        for item in list:
            for city in city_list:
                if item in city:
                    print("Entity", item,"is a city.")
                    ok = True
            if ok == False:
                cities = self._find_cities(idct, item)
                if len(cities) > 0:
                    print("Entity", item, "may be on cities:", cities)
                else: 
                    cities = self._find_cities(sdic, item)
                    if len(cities) > 0:
                        print("Entity", item, "may be on cities:", cities)
                    else: 
                        cities = self._find_cities(mdic, item)
                        if len(cities) > 0:
                            print("Entity", item, "may be on cities:", cities)
                        else:
                            print(":(")
            ok = False

