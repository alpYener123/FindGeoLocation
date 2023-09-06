# This class is for finding location entities in a given tweet

from unidecode import unidecode
from langdetect import detect
import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class EntityExtractor:

    def __init__(self, tweet):
        self.nlp = spacy.load('en_core_web_lg') # english language model
        self.tokenizer = AutoTokenizer.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish") # turkish language model
        self.model = AutoModelForTokenClassification.from_pretrained("busecarik/bert-loodos-sunlp-ner-turkish")
        self.clf = pipeline("ner", model=self.model, tokenizer=self.tokenizer)
        self.tweet = tweet # the sentence that is to be processed


    # detects the language and returns it
    def detect_lang(self):
        lang = detect(self.tweet)
        print("Language of the text:", lang)
        return lang

    # returns a list of location entities in the sentence
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

    # returns the common segment of two strings
    def _find_common_part(self, X, Y, num = 0):
        common_part = ""
        if num < 0:
            X = X[:num]
            Y = Y[:num]

        if X in Y:
            start_index = Y.index(X)
            common_part = Y[start_index:start_index + len(X)]

        return common_part

    # finds the cities that string may be linked to, returns the cities as a string
    def _recursive_search(self, sub_dict, st, cities, city=""):
        for key, value in sub_dict.items():
            if isinstance(value, dict):
                cities = self._recursive_search(value, st, cities, key)
            elif city not in cities:
                if "g" in st: # due to examples such as Ayvalık --> Ayvalığa (though wrong usage of Turkish, may still occur)
                    if key[:-2] in st[:-2]:
                        common = self._find_common_part(key, st, num = -2)
                        if len(common) + 4 >= len(st) and common[0] == st[0]:
                            cities+=(city+",")
                else:
                    if key in st: # len(common) + 4 since examples like "beylikduzunden" --> "beylikduzu" may occur where the entity gains 4 additional letters
                        common = self._find_common_part(key, st)
                        if len(common) + 4 >= len(st) and common[0] == st[0]:
                            cities+=(city+",")
                    
        return cities

    # returns a list of the cities found in the function recursive search
    def _find_cities(self, dct, target_string):
        common = ""
        common = self._recursive_search(dct, target_string, common)
        if len(common) > 0:
            common = common[:-1] # remove the last comma
            common = common.split(",")
        return common

    # prints the cities the given sentence may have mentioned by linking the districts and streets to the city itself
    def show_cities(self, city_list, idct, sdic, mdic, list):
        ok = False
        for item in list:
            for city in city_list:
                if city in item:
                    print("Entity", item,"is the city", city, ".")
                    ok = True # if we have found the city, no need to continue checking
            if ok == False:
                cities = self._find_cities(idct, item)
                if len(cities) > 0:
                    print("Entity", item, "may be on cities:", cities,". Entity is a part of the city called \"ilçe\"." )
                else: 
                    cities = self._find_cities(sdic, item)
                    if len(cities) > 0:
                        print("Entity", item, "may be on cities:", cities,". Entity is a part of the city called \"semt\".")
                    else: 
                        cities = self._find_cities(mdic, item)
                        if len(cities) > 0:
                            print("Entity", item, "may be on cities:", cities,". Entity is a part of the city called \"mahalle\".")
                        else:
                            print("No corresponding city has found for entity", item,". :(")
            ok = False



# DELETE THE BELOW PART
    
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
                    return_list.append(add[:-1])
    
    
    def _is_substring_in_nested_dict(self, dct, target_string, check=False, city = ""):

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