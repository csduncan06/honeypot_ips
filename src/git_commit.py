import json
import base64
import requests


CONFIG_FILE = 'config.json'

ACCESS_TOKEN = None
USERNAME = None
REPO_NAME = None
FILE_PATH = None
BRANCH = None


def read_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def upload_file_to_github(file_path, content, message, USERNAME, REPO_NAME, ACCESS_TOKEN):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{file_path}'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    content_base64 = base64.b64encode(content.encode()).decode()

    if 'sha' in response_json:
        data = {
            'message': message,
            'content': content_base64,
            'sha': response_json['sha'],
            'branch': BRANCH
        }
        response = requests.put(url, headers=headers, json=data)
    else:

        data = {
            'message': message,
            'content': content_base64,
            'branch': BRANCH
        }
        response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print('File uploaded successfully!')
    else:
        print('Error uploading file:', response.content)
        
def UPLOAD(total_new_ips):
    global ACCESS_TOKEN, USERNAME, REPO_NAME, FILE_PATH, BRANCH

    try:
        config = read_config(CONFIG_FILE)
        ACCESS_TOKEN = config.get('ACCESS_TOKEN')
        USERNAME = config.get('USERNAME')
        REPO_NAME = config.get('REPO_NAME')
        FILE_PATH = config.get('FILE_PATH')
        BRANCH = config.get('BRANCH')

        with open('honeypot_ips.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()

        commit_message = f"auto updated {total_new_ips} honeypot ips"
        upload_file_to_github(FILE_PATH, file_content, commit_message, USERNAME, REPO_NAME, ACCESS_TOKEN)
    except Exception as e:
        print(e)



