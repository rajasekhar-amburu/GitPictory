from pymongo import MongoClient

# Replace 'localhost' and '27017' with your MongoDB host and port
client = MongoClient('mongodb://localhost:27017/')

# Connect to the specific database
db = client['pictoryTemplates']

# Create a new collection (if it doesn't exist)
collection = db['defaultTemplates']

import json
file_path = "C:\\Users\\Rajasekhar\\PycharmProjects\\Pictory_Selenium\\templates.json"

# Open the JSON file and load the data
with open(file_path, 'r') as file:
    data = json.load(file)

all_templates = data['templates']['Items']

complete_doc= dict()
for each_template in all_templates:
    key = each_template['metaData']['name']
    value = 'template_' + each_template['metaData']['id']
    print(key,',',value)
    complete_doc[key] = value

print("complete_doc", complete_doc)