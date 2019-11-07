import os
import json

id_url_map = {}
index = 1
for root, dirs, files in os.walk('./DEV'):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file), 'r') as json_file:
                json_obj = json.load(json_file)
                id_url_map[index] = json_obj['url']
                index += 1

print(id_url_map)