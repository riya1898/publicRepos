-- DROP TABLE repository;
-- DROP TABLE userpages;
CREATE TABLE IF NOT EXISTS repository(id INT NOT NULL, username TEXT NOT NULL, respositoryname TEXT);
CREATE TABLE IF NOT EXISTS userpages(username TEXT NOT NULL, pagenumber INT);