import MySQLdb

user = "www"
passwd = "geek"
dbname = "nessus"

def getDB():
    db = MySQLdb.connect("localhost",user,passwd,dbname)
    c = db.cursor()
    return c