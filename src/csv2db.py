# data/ 위치에 있는 CSV파일을 전부 db에 넣음
# 파일 이름에 generated_ 를 앞에 붙여서 db에 저정함

import pandas as pd
from sqlalchemy import create_engine

# DB 정보 개인 환경에 맟춰서 넣어주세요오
username = "root"
password = "password"
host = "localhost"
database = "demo"

engine = create_engine(
    f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
)

# 파일 이름 잘 확인해주세요.. 이름 다른거 있으면 바꿔야해용
filenames = ["links", "movies", "scrapping", "ratings", "tags"]

for filename in filenames:
    csv_file_path = f"data/{filename}.csv"
    df = pd.read_csv(csv_file_path)

    df.to_sql(
        name="generated_" + filename, con=engine, index=False, if_exists="replace"
    )

    print(
        f"Table '{filename}' has been created and populated with data from '{csv_file_path}'."
    )
