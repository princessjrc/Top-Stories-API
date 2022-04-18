import streamlit as st
import numpy as np
import pandas as pd
import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions

nltk.download("punkt")
nltk.download("stopwords")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("COP 4813 - Web Application Programming")

st.title("Project 1")

st.header("Part A - The Stories API")

st.write("This app uses the Top Stories API to display the most common words used in the top "
         "current articles based on a specified topic selected by the user. The data is "
         "displayed as a line chart and as a wordcloud image.")

st.subheader("I - Topic Selection")

user_input = st.text_input("Please enter your name.")

option = st.selectbox(
    "Select a topic of interest.",
    ["arts", "automobiles", "books", "business", "fashion", "food", "health",
     "home", "insider", "magazine", "movies", "nyregion", "obituaries", "opinion",
     "politics", "realestate", "science", "sports", "sundayreview", "technology",
     "theater", "t-magazine", "travel", "upshot", "us", "world"]
)

"Hi " + user_input + ", you selected the ", option, "topic."

api_key_dict = main_functions.read_from_file("JSON.files/api_key.json")
api_key = api_key_dict["my_key"]

url = "https://api.nytimes.com/svc/topstories/v2/" + option + ".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON.files/response.json")

my_articles = main_functions.read_from_file("JSON.files/response.json")

str1 = ""

for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

sentences = sent_tokenize(str1)

words = word_tokenize(str1)

fdist = FreqDist(words)

words_no_punc = []

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

fdist2 = FreqDist(words_no_punc)

stopwords = stopwords.words("english")

clean_words = []

for w in words_no_punc:
    if w not in stopwords and w != 'new':
        clean_words.append(w)

st.subheader("II - Frequency Distribution")

wordcloud = WordCloud().generate(str1)

fdist3 = FreqDist(clean_words)

most_freq = fdist3.most_common(10)

if st.checkbox("Click here to generate frequecy distribution."):
    freq_words = [i[0] for i in most_freq]
    occurrences = [i[1] for i in most_freq]

    fig, ax = plt.subplots()
    ax.plot(freq_words, occurrences, color='green')
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.title("Frequency Distribution Chart")
    st.pyplot(fig)

st.subheader("III - Wordcloud")
if st.checkbox("Click here to generate wordcloud."):
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)

st.header("Part B - Most Popular Articles")

st.write("Select if you want to see the most shared, emailed, or viewed articles.")

option2 = st.selectbox(
    "Select your preferred set of articles.",
    ["shared", "emailed", "viewed"]
)

option3 = st.selectbox(
    "Select the period of time (last # of days).",
    ["1", "7", "30"]
)

url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + option3 + ".json?api-key=" + api_key

response2 = requests.get(url2).json()

main_functions.save_to_file(response2, "JSON.files/response2.json")

my_articles2 = main_functions.read_from_file("JSON.files/response2.json")

str2 = ""

for i in my_articles["results"]:
    str2 = str2 + i["abstract"]

words2 = word_tokenize(str2)

fdist = FreqDist(words2)

words_no_punc = []

for w in words2:
    if w.isalpha():
        words_no_punc.append(w.lower())

fdist2 = FreqDist(words_no_punc)

clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

fdist3 = FreqDist(clean_words)

wordcloud = WordCloud().generate(str2)

fig, ax = plt.subplots()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(fig)