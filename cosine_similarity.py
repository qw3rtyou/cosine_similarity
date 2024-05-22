from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# 데이터 로딩 및 TF-IDF 계산
data = pd.read_csv("data/scrapping.csv", low_memory=False)
data["Overview"] = data["Overview"].fillna("")
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(data["Overview"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
title_to_index = dict(zip(data["Movie ID"], data.index))


@app.route("/recommend", methods=["GET"])
def recommend():
    movie_id = request.args.get("mvid", type=int)
    if movie_id not in title_to_index:
        return jsonify({"error": "Movie ID not found in dataset"}), 404

    recommendations = get_recommendations(movie_id)
    result = data.loc[recommendations, "Movie ID"].tolist()
    return jsonify(result)


def get_recommendations(movieId, cosine_sim=cosine_sim):
    idx = title_to_index[movieId]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [idx[0] for idx in sim_scores]
    return data.index[movie_indices]


if __name__ == "__main__":
    app.run(debug=True)
