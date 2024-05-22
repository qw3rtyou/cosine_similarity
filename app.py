from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

data = pd.read_csv("data/scrapping.csv", low_memory=False)
data["Overview"] = data["Overview"].fillna("")
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(data["Overview"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
title_to_index = dict(zip(data["Movie ID"], data.index))


@app.route("/recommend", methods=["POST"])
def recommend():
    movie_ids = request.json.get("movie_ids")
    if not all(movie_id in title_to_index for movie_id in movie_ids):
        return jsonify({"error": "One or more Movie IDs not found in dataset"}), 404

    combined_overview = " ".join(data.loc[data["Movie ID"].isin(movie_ids), "Overview"])
    tfidf_vector = tfidf.transform([combined_overview])
    sim_scores = cosine_similarity(tfidf_vector, tfidf_matrix).flatten()
    sim_scores_indices = sim_scores.argsort()[-26:-1][::-1]

    recommended_movie_ids = (
        data[["Movie ID", "Original Title", "Overview", "Poster Path"]]
        .iloc[sim_scores_indices]
        .to_dict("records")
    )

    # recommended_movie_ids에서 필요한거 뽑아다 쓰면 됨
    result = [
        {
            "movieId": movie["Movie ID"],
            "moviePhotoUrl": movie["Poster Path"],
        }
        for movie in recommended_movie_ids
    ]
    return jsonify(result)


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
