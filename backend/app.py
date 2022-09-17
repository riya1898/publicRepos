
import sqlite3
from flask import Flask, render_template
import json
from pip._vendor import requests
from flask import request
from flask_cors import CORS, cross_origin
from datetime import datetime
from datetime import datetime


app = Flask(__name__)
CORS(app, support_credentials=True)
data = []
repositoryDataFromDb = []
perPageRecs = 30
userData = []

def createDb():
    con = sqlite3.connect("repository.db")
    with open('schema.sql') as f:
        con.executescript(f.read())

# def storeData(github_username, pageNumber):
#     con = sqlite3.connect("repository.db")
#     cur = con.cursor()
#     api_url1 = f"https://api.github.com/users/{github_username}/repos?per_page={perPageRecs}&page={pageNumber + 1}"
    
#     response1 = requests.get(api_url1)
#     data1 =  response1.json()
#     # store data into repository database

#     start = pageNumber * perPageRecs

#     for repository in data1:
#         key = github_username
#         value = repository["name"]
#         url = repository["html_url"]
#         desc = repository["description"]
#         createdAt = repository["created_at"]
#         cur.execute("INSERT INTO repository(id, username, respositoryname, repositoryURL, details, createdAt) VALUES(?,?,?,?,?,?)", (start, key, value, url, desc, createdAt))
#         start = start+1

#     con.commit()
#     con.close()

def storeData(github_username):
    con = sqlite3.connect("repository.db")
    cur = con.cursor()
    pageNumber = 1
    start = 0
    while(True):
        api_url1 = f"https://api.github.com/users/{github_username}/repos?page={pageNumber}"        
        pageNumber+=1
        response1 = requests.get(api_url1)
        data1 =  response1.json()
        if(len(data1)==0):
            break
        for repository in data1:
            key = github_username
            value = repository["name"]
            url = repository["html_url"]
            desc = repository["description"]
            createdAt = repository["created_at"]
            cur.execute("INSERT INTO repository(id, username, respositoryname, repositoryURL, details, createdAt) VALUES(?,?,?,?,?,?)", (start, key, value, url, desc, createdAt))
            start += 1
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
    print("here",pageNumber)
    for p in pageNumber:
        page = p[1]
        return page
    return -1


def configurePage(uname, pagelabel):
    page = getPageNumber(uname)
    con = sqlite3.connect("repository.db")
    cur = con.cursor()
    # print(page)
    if page == -1:
        print("inside if")
        page = 0
        cur.execute("INSERT INTO userpages(username, pagenumber)  VALUES(?,?)", (uname, 0))
    
    else :
        if pagelabel == "n":
            page = page + 1
        elif pagelabel == "p" and page > 0:
            page = page -1
        elif pagelabel == "d" :
            page = 0
        cur.execute("UPDATE userpages SET pagenumber=? where username =?", (page, uname))
    con.commit()
    con.close()
    return page


def validateDate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "YYYY-MM-DD").strftime('YYYY-MM-DD'):
            raise ValueError
        return True
    except ValueError:
        return False


@app.route('/home/',  methods=('GET', 'POST'))
@cross_origin(supports_credentials=True)
def index():
    userData = []
    res = True
    args = request.args
    uname = args['uname']
    pageLabel = args['page']
    date = args['date']
    createDb()
    print("date", date)
    
    if validateDate(date):
        print("date validated")
        res = True
    else:
        res = False

    if pageLabel == 'n' or pageLabel == 'p' or pageLabel == 'd' and res == True :
        print("condition1")
        pageNumber = configurePage(uname, pageLabel)
        userData = getData(uname, pageNumber, date)
    
        if len(userData) == 0:
            storeData(uname)
            userData = getData(uname, pageNumber, date)
    
        print(userData)
    return userData


def getData(uname, pageNumber, date):
    getRepoData = []

    con = getDbConnection()
    cur = con.cursor() 

    start = pageNumber * perPageRecs
    end = start + perPageRecs
    print(date)
    # publicRepository = cur.execute("SELECT * FROM repository WHERE username = '"+uname+"' AND id BETWEEN '"+str(start)+"' AND '"+str(end)+"' ").fetchall()
    # print("publicRepository")
    publicRepository = cur.execute("SELECT DISTINCT * FROM repository where username = '"+uname+"' and createdAt >= '"+date+"' ORDER BY createdAt LIMIT '"+str(perPageRecs)+"' OFFSET '"+str(start)+"' ").fetchall()
    print("SELECT * FROM repository where username = '"+uname+"' and createdAt >= '"+date+"' ORDER BY createdAt LIMIT '"+str(perPageRecs)+"' OFFSET '"+str(start)+"' " )
    # print(publicRepository)
    con.commit()
    con.close()
    
    for row in publicRepository:
        repoDataJson = { }
        repoDataJson['username'] =row[1]
        repoDataJson['repositoryName'] = row[2]
        repoDataJson['repoURL'] = row[3]
        repoDataJson['description'] = row[4]
        repoDataJson['createdAt'] = row[5]

        getRepoData.append(repoDataJson)

    
    # print(getRepoData)
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


