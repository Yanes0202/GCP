from google.cloud import storage
 
client = storage.Client()
 
bucket = client.bucket('gcp-my-unique-bucket')
for o in client.list_blobs(bucket):
    o.download_to_filename(f"./bucket/{o.name}")
    print("Object name: %s" % o.name)