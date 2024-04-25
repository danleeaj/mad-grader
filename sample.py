import requests

rubric_component = "Amyloid beta plaques and neurofibrillary tangles are hallmarks of Alzheimer's."
student_response = "The histopathological hallmarks of Alzheimer's include amyloid beta plaque build-up and tau neurofibrillary tangle formation. They cause GluA2 receptor loss through causing receptor endocytosis."

BASE = "https://ipyvvhizmh.execute-api.us-east-2.amazonaws.com/test/"

response = requests.get(f"{BASE}debate?rubric_component={rubric_component}&student_response={student_response}")

print(response.json())