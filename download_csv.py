import requests
import zipfile
import os
import shutil

url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
zip_path = "ml-latest-small.zip"
extract_folder = "data"

if not os.path.exists(extract_folder):
    os.makedirs(extract_folder)

response = requests.get(url)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    with open(zip_path, "wb") as file:
        file.write(response.content)
else:
    print("Failed to download file.")

try:
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                continue

            source = zip_ref.open(member)
            target = os.path.join(extract_folder, filename)

            with open(target, "wb") as f:
                shutil.copyfileobj(source, f)

    print("Extraction complete.")
except zipfile.BadZipFile:
    print("Failed to unzip file. It may be corrupted.")
