import sqlite3
from flask import Flask, render_template
import json
from pip._vendor import requests

app = Flask(__name__)
data = []
repositoryDataFromDb = []

# github_username = alex
github_username  = input("Enter Github username: ")   
print(github_username)

print("before username")
con = sqlite3.connect("repository.db")

with open('schema.sql') as f:
    con.executescript(f.read())

cur = con.cursor()

print("after connection")
#api url to grab public user repositories
api_url = f"https://api.github.com/users/{github_username}/repos"

#send request to Github API to get data
response = requests.get(api_url)

#response comes as JSON data
data =  response.json()

#store data into repository database
for repository in data:
    # print(repository["name"])
    key = github_username
    value = repository["name"]
    cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))

con.commit()
con.close()


def getDbConnection():
    con = sqlite3.connect('repository.db')
    # con.row_factory = sqlite3.Row
    return con


@app.route('/home')
def index():
    con = getDbConnection()
    cur = con.cursor()
    publicRepository = cur.execute('SELECT * FROM repository;').fetchall()
    print("Repos from git",publicRepository)
    con.commit()
    con.close()
    for row in publicRepository:
        # dataString = json.dumps([x for x in row])
        # print(dataString)
        # data.append(dataString)
        # print(data)
        repositoryDataFromDb.append(row)
    print(repositoryDataFromDb)
    return repositoryDataFromDb