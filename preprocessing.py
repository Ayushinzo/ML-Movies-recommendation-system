import pandas as pd
from json import dumps
from sklearn.feature_extraction.text import TfidfVectorizer

from utility import get_names, get_character_name, get_director, stem

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

dataset = None

title_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
person_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
metadata_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)

title_vectors = None
person_vectors = None
metadata_vectors = None

def join_names(names):
    return " ".join([name.replace(" ", "") for name in names])

def preprocessing():
    global dataset
    global title_vectors, person_vectors, metadata_vectors

    dataset = movies.merge(credits, on="title")

    dataset = dataset[
        ["movie_id", "title", "genres", "keywords", "overview", "cast", "crew"]
    ]

    dataset.dropna(inplace=True)

    dataset["genres"] = dataset["genres"].apply(get_names)
    dataset["keywords"] = dataset["keywords"].apply(get_names)
    dataset["cast"] = dataset["cast"].apply(get_character_name)
    dataset["crew"] = dataset["crew"].apply(get_director)

    dataset["title_clean"] = dataset["title"].str.lower().str.strip()

    dataset["director_text"] = dataset["crew"].apply(join_names).str.lower()
    dataset["cast_text"] = dataset["cast"].apply(join_names).str.lower()

    dataset["people_text"] = (
        dataset["director_text"] + " " + dataset["cast_text"]
    )

    dataset["metadata_text"] = (
        dataset["genres"].apply(lambda x: " ".join(x)) + " " +
        dataset["keywords"].apply(lambda x: " ".join(x)) + " " +
        dataset["overview"]
    )

    dataset["metadata_text"] = dataset["metadata_text"].str.lower().apply(stem)

    title_vectors = title_vectorizer.fit_transform(dataset["title_clean"])
    person_vectors = person_vectorizer.fit_transform(dataset["people_text"])
    metadata_vectors = metadata_vectorizer.fit_transform(dataset["metadata_text"])

    print("Preprocessing completed successfully.")