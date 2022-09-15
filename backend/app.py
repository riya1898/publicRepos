
import sqlite3
from flask import Flask, render_template
import json
from pip._vendor import requests
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
data = []
repositoryDataFromDb = []

perPageRecs = 30

def createDb():
    con = sqlite3.connect("repository.db")
    with open('schema.sql') as f:
        con.executescript(f.read())

def storeData(github_username, pageNumber):
    con = sqlite3.connect("repository.db")
    cur = con.cursor()
    api_url1 = f"https://api.github.com/users/{github_username}/repos?per_page={perPageRecs}&page={pageNumber + 1}"
    # api_url2 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=2"
    # api_url3 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=3"

    response1 = requests.get(api_url1)
    # print(response1.json(), "response")
    data1 =  response1.json()

    # response2 = requests.get(api_url2)
    # print(response2.json(), "response")
    # data2 =  response2.json()

    # response3 = requests.get(api_url3)
    # print(response3.json(), "response")
    # data3 =  response3.json()
    # store data into repository database

    start = pageNumber * perPageRecs

    for repository in data1:
        key = github_username
        value = repository["name"]
        cur.execute("INSERT INTO repository(id, username, respositoryname) VALUES(?,?,?)", (start, key, value))
        start = start+1
    # for repository in data2:
    #     key = github_username
    #     value = repository["name"]
    #     cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))
    
    # for repository in data3:
    #     key = github_username
    #     value = repository["name"]
    #     cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))

    con.commit()
    con.close()


def getDbConnection():
    con = sqlite3.connect('repository.db')
    # con.row_factory = sqlite3.Row
    return con

def getPageNumber(uname):
    con = sqlite3.connect("repository.db")
    cur = con.cursor()
    pageNumber = cur.execute("SELECT * FROM userpages WHERE username= '"+uname+"' ").fetchall()
    # print("here",pageNumber)
    for p in pageNumber:
        page = p[1]
        return page
    return 0


def configurePage(uname, pagelabel):
    page = getPageNumber(uname)
    con = sqlite3.connect("repository.db")
    cur = con.cursor()
    # print(page)
    if page == -1:
        # print("inside if")
        page = 0
        cur.execute("INSERT INTO userpages(username, pagenumber)  VALUES(?,?)", (uname, 0))
    
    else :
        if pagelabel == "n":
            page = page + 1
        elif pagelabel == "p":
            page = page -1
        cur.execute("UPDATE userpages SET pagenumber=? where username =?", (page, uname))
    con.commit()
    con.close()
    return page

@app.route('/home/',  methods=('GET', 'POST'))
@cross_origin(supports_credentials=True)
def index():
    args = request.args
    uname = args['uname']
    pageLabel = args['page']
    createDb()
    print("pagelabel", pageLabel)
    pageNumber = configurePage(uname, pageLabel)
    if pageLabel =="p" and pageNumber > 0:
        pageNumber-= 1
    
    elif pageLabel == "n":
        pageNumber+= 1

    userData = getData(uname, pageNumber)
    if len(userData) == 0:
        storeData(uname, pageNumber)
        userData = getData(uname, pageNumber)
    
    # print(userData)
    return userData


def getData(uname, pageNumber):
    getRepoData = []
    con = getDbConnection()
    cur = con.cursor() 

    start = pageNumber * perPageRecs
    end = start + perPageRecs

    # print(start)
    # print(end)

    publicRepository = cur.execute("SELECT * FROM repository WHERE username = '"+uname+"' AND id BETWEEN '"+str(start)+"' AND '"+str(end)+"' ").fetchall()
    # print("publicRepository")
    con.commit()
    con.close()
    
    for row in publicRepository:
        getRepoData.append(row)
    
    return getRepoData










# import sqlite3
# from flask import Flask, render_template
# import json
# from pip._vendor import requests

# app = Flask(__name__)
# repositoryDataFromDb = []

# def storeData(github_username):
#     print("inside storedata")
#     con = sqlite3.connect("repositoryDetails.db")
#     with open('schema.sql') as f:
#         con.executescript(f.read())
#     cur = con.cursor()
#     api_url1 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=1"
#     # api_url2 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=2"
#     # api_url3 = f"https://api.github.com/users/{github_username}/repos?per_page=100&page=3"

#     response1 = requests.get(api_url1)
#     print(response1.json(), "response")
#     data1 =  response1.json()

#     # response2 = requests.get(api_url2)
#     # print(response2.json(), "response")
#     # data2 =  response2.json()

#     # response3 = requests.get(api_url3)
#     # print(response3.json(), "response")
#     # data3 =  response3.json()
#     # # store data into repository database

#     for repository in data1:
#         key = github_username
#         value = repository["name"]
#         cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))
    
#     # for repository in data2:
#     #     key = github_username
#     #     value = repository["name"]
#     #     cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))
    
#     # for repository in data3:
#     #     key = github_username
#     #     value = repository["name"]
#     #     cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))

#     con.commit()
#     con.close()


# def getDbConnection():
#     con = sqlite3.connect('repositoryDetails.db')
#     # con.row_factory = sqlite3.Row
#     return con


# @app.route('/home/<uname>',  methods=('GET', 'POST'),)
# def index(uname):
#     userData = getData(uname)
#     print(uname)
#     if len(userData) == 0:
#         storeData(uname)
#         userData = getData(uname)
    
#     print(userData)
#     return userData

# def getData(uname):
#     getRepoData = []
#     con = getDbConnection()
#     cur = con.cursor()
#     publicRepository = cur.execute("SELECT * FROM repositoryDetails WHERE username = '"+uname+"'").fetchall()
#     con.commit()
#     con.close()
    
#     for row in publicRepository:
#         getRepoData.append(row)
    
#     return getRepoData


