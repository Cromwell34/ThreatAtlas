import pandas as pd
import string
import pandas as pd
import spacy
import feedparser
import plotly.graph_objs as go
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import plotly.graph_objs as go

nlp = spacy.load("en_core_web_trf")
path = "test_feeds.csv"


def fetch_articles_from_rss(feed_url, source):
    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries:
        articles.append(entry)

    return articles


def get_content(path):
    feed_db = pd.read_csv(path)

    # zip relevant cols
    reqs = list(zip(feed_db["feed_name"].tolist(), feed_db["feed_url"].tolist()))
    # fetch articles

    article_dump = []
    for req in reqs:
        articles = fetch_articles_from_rss(req[1], req[0])
        article_dump.append((req[0], articles))
        # print("  ")
        # print("Fetched successfully "+"feed: "+req[0])
        # print([article['title'] for article in articles])

    return dict(article_dump)


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def output_to_csv(sources, data):
    dump = []
    for source in sources:
        for article_ in data[source]:
            article = dict(article_)
            dump.append(article)

    test_db = pd.DataFrame(dump)
    test_db.to_csv("test_output.csv")
    return test_db


def extract_countries(article):
    doc = nlp(article)
    countries = []

    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "NORP" or ent.label_ == "LOC":
            countries.append(ent.text)

    return list(set(countries))


def extract_individuals(article):
    doc = nlp(article)
    individuals = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            individuals.append(ent.text)

    return list(set(individuals))


def extract_organizations(article):
    doc = nlp(article)
    organizations = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            organizations.append(ent.text)

    return list(set(organizations))


def key_phrases(article):
    phrases = []
    doc = nlp(article)
    for chunk in doc.noun_chunks:
        phrases.append(chunk)

    return phrases


def extract_event(article):
    countries = extract_countries(article)
    individuals = extract_individuals(article)
    organizations = extract_organizations(article)
    phrases = key_phrases(article)
    url = None

    current_event = {
        "countries_involved": countries,
        "associated_individuals": individuals,
        "associated_organizations": organizations,
        "key_phrases": phrases,
    }

    return current_event


articles = []
headers = [
    "Countries involved",
    "Date",
    "Associated Individuals",
    "Associated Organizations",
    "Countries Involved",
    "Location",
    "url",
]


def eventlist(articles):
    events = pd.dataframe(names=headers)
    for article in articles:
        extract_event(article)

    return events


def flat_ents1(ents):
    flat_ents = []
    for ent in ents:
        flat_ents = flat_ents + ent[1]

    return flat_ents


def new_count(field, frame):
    indexed = list(zip(list(range(len(frame[field].tolist()))), frame[field].tolist()))
    all_ = flat_ents1(indexed)
    counted_ = {i: all_.count(i) for i in all_}
    counted = sorted(counted_.items(), key=lambda x: x[1], reverse=True)

    return counted


def flat_ents1(ents):
    flat_ents = []
    for ent in ents:
        flat_ents = flat_ents + ent[1]

    return flat_ents


def new_count(field, frame):
    indexed = list(zip(list(range(len(frame[field].tolist()))), frame[field].tolist()))
    all_ = flat_ents1(indexed)
    counted_ = {i: all_.count(i) for i in all_}
    counted = sorted(counted_.items(), key=lambda x: x[1], reverse=True)

    return counted


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def get_summaries(headlines, df):
    summaries = []
    for headline in headlines[0]:
        summaries.append(df.loc[df["Title"] == headline]["Summary"].to_list())

    return flatten_list(summaries)


def top_n_bar_chart(data, n, var_name, vertical):
    if vertical == True:
        y = [k[0] for k in data[1:n]]
        x = [k[1] for k in data[1:n]]
        data = [go.Bar(x=x, y=y, orientation="h")]
        layout = go.Layout(title=f"Top {n} " + var_name, template="plotly_dark")
        fig = go.Figure(data=data, layout=layout)
        fig.show()

    else:
        x = [k[0] for k in data[1:n]]
        y = [k[1] for k in data[1:n]]
        data = [go.Bar(x=x, y=y)]
        layout = go.Layout(title=f"Top {n} " + var_name, template="plotly_dark")
        fig = go.Figure(data=data, layout=layout)
        fig.show()


def country_headlines(country, df):
    headlines = df.loc[df["country"] == country]["headlines"]

    return headlines


def extract_ngrams(article, n):
    # Tokenize the article into words
    tokens = nltk.word_tokenize(article)

    # Generate the N-grams
    n_grams = ngrams(tokens, n)

    # Count the N-grams
    n_gram_counts = Counter(n_grams)

    return n_gram_counts


def clean_stopwords(article):
    # Tokenize the article into words
    tokens = word_tokenize(article)

    # Get the English stopwords
    stop_words = set(stopwords.words("english"))

    # Filter out the stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Join the filtered tokens back into a string
    cleaned_article = " ".join(filtered_tokens)

    return cleaned_article


def aggregate_ngrams(articles, n):
    ngrams = []
    for article in articles:
        a = clean_stopwords(article).translate(
            str.maketrans("", "", string.punctuation)
        )

        for k in extract_ngrams(a, n).keys():
            ngrams.append(k)

    return Counter(ngrams)


def country_ngrams(country, master, n):
    summaries = get_summaries(country, master)
    n_gram_counts = dict(
        sorted(
            aggregate_ngrams(summaries, n).items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    return n_gram_counts


def get_entities(headlines, df, type_):
    ents_nested = []
    ents = []

    for headline in headlines[0]:
        ents_nested.append(df.loc[df["Title"] == headline][type_].to_list())

    for li in ents_nested:
        for li2 in li:
            for e in li2:
                ents.append(e)

    return (sorted(Counter(ents).items(), key=lambda item: item[1], reverse=True), ents_nested)