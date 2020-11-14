import requests
import json


def create_employee(endpoint, data=None):
    response = requests.post(endpoint, json=data)
    print(response)
    print(response.content)


def list_courses(endpoint):
    response = requests.get(endpoint)
    print(response)
    print(json.loads(response.content))


def delete(endpint):
    res = requests.delete(endpint)
    print(res)
    print(res.content)


def download_image():
    response = requests.get('https://lh3.googleusercontent.com/ogw/ADGmqu8BVI77DUTloFg17ruBnFvHmN9eGF7mESvv13VY=s128-b16-cc-rp-mo')
    print(response.status_code)
    with open('profile.png', 'wb') as f:
        f.write(response.content)


# create_employee('http://127.0.0.1:5000/post', data={'ID': 343, 'Name': 'Mohammed Ali', 'Salary': 3430.43})
# list_courses('http://127.0.0.1:5000/api-3/')  # list all course
# list_courses('http://127.0.0.1:5000/api/111')   # get single course with id 111
# delete('http://127.0.0.1:5555/api-flask-restplus/13')
# download_image()
