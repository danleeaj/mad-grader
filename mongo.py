from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from debate import debate

uri = "mongodb+srv://danleeaj0512:mXDytEn9UWN5PHp4@debate-test.oii4eon.mongodb.net/?retryWrites=true&w=majority&appName=debate-test"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["debates-db"]
col = db["debates"] # db.debates is also ok, but doing it dict style to keep it consistent

rubric_component = "Amyloid beta plaques and neurofibrillary tangles are hallmarks of Alzheimer's."

student_response = "The histopathological hallmarks of Alzheimer's include amyloid beta plaque build-up and tau neurofibrillary tangle formation. They cause GluA2 receptor loss through causing receptor endocytosis."

response = debate(rubric_component, student_response)

id = col.insert_one(response.toDICT()).inserted_id
print(id)

# posts = db.posts
# post_id = posts.insert_one(post).inserted_id

# print(post_id)