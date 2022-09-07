import sqlite3
from pip._vendor import requests

# github_username = alex
github_username  = input("Enter Github username: ")   
print(github_username)

print("before username")
con = sqlite3.connect("repository.db")

with open('schema.sql') as f:
    con.executescript(f.read())

cur = con.cursor()

print("after connection")
# cur.execute("CREATE TABLE IF NOT EXISTS repository(username, respositoryname)")
#api url to grab public user repositories
api_url = f"https://api.github.com/users/{github_username}/repos"

#send request to Github API to get data
response = requests.get(api_url)

#response comes as JSON data
data =  response.json()

#store data into repository database
for repository in data:
    print(repository["name"])
    key = github_username
    value = repository["name"]
    cur.execute("INSERT INTO repository(username, respositoryname) VALUES(?,?)", (key, value))

# for row in cur.execute('SELECT * FROM repository;'):
#     print(row)

con.commit()
con.close()

