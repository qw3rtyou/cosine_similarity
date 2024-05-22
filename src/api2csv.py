# https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg
# tmdb api를 이용해서 스크래핑 하는 스크립트
# 나중에 필요한 컬럼있으면 response json 파싱 다시 해서 추가하시면 됩니당
# 속도 꽤 빠름 전체 데이터 20만개가 안되서 3분도 안걸림

# ------------ round 1 ----------
# 너무 느림

# import requests
# import pandas as pd

# link_df = pd.read_csv("original_data/links.csv")


# def tmdbId2json(tmdbId):
#     url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key=1f22f645dd0f53f65e833307729cbc9c"
#     response = requests.get(url=url)

#     if response.status_code == 200:
#         data = response.json()
#         original_title = data.get("original_title")
#         overview = data.get("overview")
#         poster_path = data.get("poster_path")

#         print(f"Movie ID: {movieId}")
#         print(f"Original Title: {original_title}")
#         print(f"Overview: {overview}")
#         print(f"Poster Path: {poster_path}")
#         print("-----")
#         # mysql저장

#     else:
#         print(f"Failed to fetch data for movie ID {movieId} with TMDb ID {tmdbId}")
#         return


# for row in link_df.itertuples():
#     movieId = row.movieId
#     tmdbId = row.tmdbId
#     tmdbId2json(tmdbId)


# ----------round 2-------------
# 스레드 기반으로 더빠르게 동작하게 만들고 바로 csv로 저장
# 저장이 불안정하고 느림


# import requests
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor

# link_df = pd.read_csv("original_data/links.csv")


# def tmdbId2json(row):
#     movieId = row.movieId
#     tmdbId = row.tmdbId
#     url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key=1f22f645dd0f53f65e833307729cbc9c"
#     response = requests.get(url=url)

#     if response.status_code == 200:
#         data = response.json()
#         original_title = data.get("original_title")
#         overview = data.get("overview")
#         poster_path = data.get("poster_path")

#         print(f"Movie ID: {movieId}")
#         print(f"Original Title: {original_title}")
#         print(f"Overview: {overview}")
#         print(f"Poster Path: {poster_path}")
#         print("-----")

#     else:
#         print(f"Failed to fetch data for movie ID {movieId} with TMDb ID {tmdbId}")
#         return


# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(tmdbId2json, link_df.itertuples())


# ---------- round 3 -------------
# 1000 단위로 나눠서 저장 csv에 제대로 저장
# 스레딩는 그대로 채택
# 빠르고 안정적
# 최종본

import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os

link_df = pd.read_csv("data/links.csv")


def fetch_data(row):
    movieId = row.movieId
    tmdbId = row.tmdbId
    url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key=1f22f645dd0f53f65e833307729cbc9c"
    response = requests.get(url=url)

    if response.status_code == 200:
        data = response.json()
        return {
            "Movie ID": movieId,
            "Original Title": data.get("original_title"),
            "Overview": data.get("overview"),
            "Poster Path": data.get("poster_path"),
        }
    else:
        print(f"Failed to fetch data for movie ID {movieId} with TMDb ID {tmdbId}")
        return None


def save_to_csv(results, filename="data/scrapping.csv"):
    df = pd.DataFrame(results)
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode="a", header=False, index=False)


all_results = []

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_data, link_df.itertuples()))
    for result in results:
        if result is not None:
            all_results.append(result)
            if len(all_results) >= 1000:
                save_to_csv(all_results)
                all_results = []

if all_results:
    save_to_csv(all_results)
