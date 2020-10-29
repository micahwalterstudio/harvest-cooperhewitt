import os
import json

import requests

CH_API_ENDPOINT="https://api.collection.cooperhewitt.org/rest/"
CH_API_TOKEN=os.environ.get("CH_API_TOKEN")

def id2path(id):

    tmp = str(id)
    parts = []

    while len(tmp) > 3:
        parts.append(tmp[0:3])
        tmp = tmp[3:]

    if len(tmp):
        parts.append(tmp)

    return os.path.join(*parts)

def rest_call(method, endpoint=CH_API_ENDPOINT, *args, **kwargs):

    params = kwargs.get('params', None)
    timeout = kwargs.get('timeout', 15)

    url = endpoint + "?method=" + method

    for key, value in params.items():
        url = url + "&" + key + "=" + str(value)
        
    r = {}
   
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout)

    except Exception as e:
        
        return e
        
    return r.json()


def write_to_json(data):
    pass


def main():
    # set up a data folder

    if not os.path.exists('data'):
        os.mkdir('data')

    departments = [35347493, 35347497, 35347501, 35347503, 35518655]
    # departments = [35518655]

    # loop through the five Cooper Hewitt departments
    for department in departments:
        print("Downloading department: ", department)

        # 1. make an API call for objects.search with the department ID

        method = "cooperhewitt.search.objects"

        params = {
            "access_token": CH_API_TOKEN,
            "department_id": department
        }

        data = rest_call(method, CH_API_ENDPOINT, params=params)
        print("Total pages to download: ", data['pages'])

        # 2. loop through additional pages and store to disk
        pages = data['pages']
        for page in range(pages):

            # 3. Get each page
            params['page'] = str(page+1)
            paged_data = rest_call(method, CH_API_ENDPOINT, params=params)
            
            # 4. Store each page to disk as individual josn obkjects
            for item in paged_data['objects']:
                print("Saving: ", item['id'])

                path = "data/" + id2path(item['id'])
                
                if not os.path.exists(path):
                    os.makedirs(path)

                filename = path + "/" + str(item['id']) + '.json'

                with open(filename, 'w') as outfile:
                    json.dump(item, outfile)

if __name__ == "__main__":
    main()
