import json
import os


def retrieve_rust_items():
    items_file_path = 'items.json'
    folder_path = 'items/'
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    all_items = list()
    for file in json_files:
        path = os.path.join(folder_path, file)
        with open(path) as f:
            try:
                data = json.load(f)
                all_items.append({'itemid': data['itemid'], 'name':data['Name'], 'image': folder_path + data['shortname']+'.png'})
            except json.JSONDecodeError as e:
                print(f'Error loading {file}: {e}')
    with open(items_file_path, 'w') as f:
        json.dump(all_items, f)
    return items_file_path
