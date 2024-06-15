import json
import os
import schedule
import time
import requests
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

key_path = os.getenv("BUCKET_PATH")
bucket_name = os.getenv("BUCKET_NAME")
server_url = os.getenv("SERVER_URL")  # Adres URL, na który wysyłamy request

credentials = service_account.Credentials.from_service_account_file(key_path)
client = storage.Client(credentials=credentials)
bucket = client.bucket(bucket_name)


def process_file(blob):
    print("checking " + blob.name)
    if blob.name.startswith("done_") or blob.name.startswith("error_"):
        return

    print("Sprawdzam rozszerzenie")
    _, extension = os.path.splitext(blob.name)
    if extension != ".json":
        new_blob = bucket.blob("error_" + blob.name)
        new_blob.upload_from_filename(blob.name)
        blob.delete()
        print(f"Invalid file extension: {blob.name}")
        return
    print("rozszerzenie ok")
    local_filename = blob.name
    blob.download_to_filename(local_filename)

    with open(local_filename, "r") as file:
        content = file.read()

    print("sprawdzam poprawnośc json")
    try:
        data = json.loads(content)
        if "first_name" not in data or "last_name" not in data:
            raise ValueError("Invalid JSON format")
    except ValueError as e:
        print("json nie jest poprawny")
        new_blob = bucket.blob("error_" + blob.name)
        new_blob.upload_from_filename(local_filename)
        blob.delete()
        print(f"Invalid JSON format in file: {blob.name}")
    else:
        print("probuje wyslac requesta")
        try:
            response = requests.post(server_url + "/add_person", json=data)
            response.raise_for_status()
            print(f"Person successfully added")
            new_blob = bucket.blob("done_" + blob.name)
            new_blob.upload_from_filename(local_filename)
            blob.delete()
        except requests.exceptions.RequestException as e:
            print("cos poszlo nie tak z requestem")
            new_blob = bucket.blob("error_" + blob.name)
            new_blob.upload_from_filename(local_filename)
            blob.delete()
            print(f"Error while sending HTTP request: {e}")
    finally:
        try:
            os.remove(local_filename)
            print(f"Deleted local file: {local_filename}")
        except OSError as e:
            print(f"Error deleting local file {local_filename}: {e}")


def check_bucket():
    print("Sprawdzanie bucketu")
    for blob in client.list_blobs(bucket):
        process_file(blob)

print("Apka działa")
schedule.every(1).minutes.do(check_bucket)

while True:
    schedule.run_pending()
    time.sleep(1)
