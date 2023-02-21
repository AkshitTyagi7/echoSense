import random
import json
import pickle
import numpy as np 
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import speech_recognition as sr

lemmatizer=WordNetLemmatizer()
intents=json.loads((open('training.json')).read())

words= pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))
model=load_model('threat-detect.h5')
def clean_up_sentence(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentnece):
    sentnece_words=clean_up_sentence(sentnece)
    bag=[0]*len(words)
    for w in sentnece_words:
        for i,word in enumerate(words):
            if word==w:
                bag[i]=1
    return np.array(bag)

def predict_class(senetence):
    bow=bag_of_words(senetence)
    res=model.predict(np.array([bow]))[0]
    Error_Threshold=0.1
    # print(bow)
    # print(res)
    results=[[i,r] for i,r in enumerate(res) if r>Error_Threshold]

    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    # print(results)
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})
    return return_list
def get_response(intents_list,intents_json):
    tag=intents_list[0]['intent']
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=random.choice(i['responses'])
            break
    return result
def guess(inputtext):
    ints=predict_class(inputtext)
    res=get_response(ints,intents)
    return(res)
