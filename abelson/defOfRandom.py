import base64
from abelson import db

def formCheck(a):
    b = []
    for x in a:
        if x == "":
            b.append('0')
        else: 
            b.append('1')
            if "0" in b:
                return False 
            else:
                return True

def fileEncode(a):
    return base64.b64encode(a.read())

def getUser (a):
    b = a.split(" ")
    c = base64.b64decode(b[1]).decode('utf-8')
    d = c.split(':')
    return d

def check(u, t):
    for a in t:
        if u[0] == a["username"] and u[1] == a["password"]:
            return True 
    return False

def LoginCheck(a):
    auth = a.headers['Authorization']
    user = getUser(auth)
    tureUser = db.get_user()

    if (check(user, tureUser)):
        return True
    else:
        return False
        
def CheckLoc(a):
    try:
        int(a["zipcode"])
        int(a["phone"])
        int(a["fax"])
        return True
    except: 
        return False
