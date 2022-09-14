import sqlite3
from flask import Flask, render_template
import json
from pip._vendor import requests

app = Flask(__name__)
data = []
repositoryDataFromDb = []


print("before username")

print("after connection")

def storeData(github_username):
    con = sqlite3.connect("repository.db")
    with open('schema.sql') as f:
        con.executescript(f.read())
    cur = con.cursor()
    api_url1 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=1"
    api_url2 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=2"
    api_url3 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=3"

    response1 = requests.get(api_url1)
    print(response1.json(), "response")
    data1 =  response1.json()

    response2 = requests.get(api_url2)
    print(response2.json(), "response")
    data2 =  response2.json()

    response3 = requests.get(api_url3)
    print(response3.json(), "response")
    data3 =  response3.json()
    # store data into repository database

    for repository in data1:
        key = github_username
        value = repository["name"]
        cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))
    
    for repository in data2:
        key = github_username
        value = repository["name"]
        cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))
    
    for repository in data3:
        key = github_username
        value = repository["name"]
        cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))

    con.commit()
    con.close()


def getDbConnection():
    con = sqlite3.connect('repository.db')
    # con.row_factory = sqlite3.Row
    return con


@app.route('/home/<uname>',  methods=('GET', 'POST'),)
def index(uname):
    userData = getData(uname)
    if len(userData) == 0:
        storeData(uname)
        userData = getData(uname)
    
    print(userData)
    return userData

def getData(uname):
    getRepoData = []
    con = getDbConnection()
    cur = con.cursor()
    publicRepository = cur.execute("SELECT * FROM repository WHERE username = '"+uname+"'").fetchall()
    con.commit()
    con.close()
    
    for row in publicRepository:
        getRepoData.append(row)
    
    return getRepoData


