from json import dumps
from sklearn.metrics.pairwise import cosine_similarity
import preprocessing
from utility import stem, extract_director_from_crew, extract_genres
from poster import get_poster

def clean_query(query):
    query = query.lower().strip()

    normal_query = query
    joined_query = query.replace(" ", "")

    return stem(normal_query + " " + joined_query)


def normalize_query(query):
    query = query.lower().strip()
    joined_query = query.replace(" ", "")
    return query, joined_query, stem(query)

def get_recommendations(query, top_n=8):
    original_query, joined_query, stemmed_query = normalize_query(query)

    title_query_vector = preprocessing.title_vectorizer.transform([original_query])
    person_query_vector = preprocessing.person_vectorizer.transform([joined_query])
    metadata_query_vector = preprocessing.metadata_vectorizer.transform([stemmed_query])

    title_score = cosine_similarity(title_query_vector, preprocessing.title_vectors).flatten()
    person_score = cosine_similarity(person_query_vector, preprocessing.person_vectors).flatten()
    metadata_score = cosine_similarity(metadata_query_vector, preprocessing.metadata_vectors).flatten()

    results = preprocessing.dataset.copy()

    results["score"] = (
        title_score * 6 +
        person_score * 4 +
        metadata_score * 2
    )

    results.loc[results["title_clean"] == original_query, "score"] += 100
    results.loc[results["title_clean"].str.startswith(original_query, na=False), "score"] += 30
    results.loc[results["title_clean"].str.contains(original_query, case=False, na=False), "score"] += 15
    results.loc[results["director_text"].str.contains(joined_query, case=False, na=False), "score"] += 40
    results.loc[results["cast_text"].str.contains(joined_query, case=False, na=False), "score"] += 25

    results = results.sort_values(by="score", ascending=False).head(top_n)

    # Remove columns that will be merged again
    for col in ["overview", "popularity", "release_date", "runtime", "vote_count", "crew", "genres"]:
        if col in results.columns:
            results.drop(columns=[col], inplace=True)

    movie_details = preprocessing.movies[
        ["id", "overview", "popularity", "release_date", "runtime", "vote_count", "genres"]
    ].copy()

    movie_details.rename(columns={"id": "movie_id"}, inplace=True)

    credits_df = preprocessing.credits[["movie_id", "crew"]].copy()

    results = results.merge(movie_details, on="movie_id", how="left")
    results = results.merge(credits_df, on="movie_id", how="left")

    results["director"] = results["crew"].apply(extract_director_from_crew)
    results["genres"] = results["genres"].apply(extract_genres)
    results["poster_url"] = results["movie_id"].apply(get_poster)

    final_df = results[
        [
            "movie_id",
            "title",
            "overview",
            "genres",
            "popularity",
            "release_date",
            "runtime",
            "director",
            "vote_count",
            "poster_url",
            "score"
        ]
    ]

    return dumps(final_df.to_dict(orient="records"), indent=4)