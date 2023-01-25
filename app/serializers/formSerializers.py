
def getuserformEntity(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "modulename": post["modulename"],
        "recuriter": post['recuriter'],
        "moduleelements": post["moduleelements"],
    }

def getmoduletabledata(post) -> dict:
    return {
      "_id": str(post["_id"]),
      "moduleId": post['moduleId'],
      "recuriter": post['recuriter'], 
      "tableData": post["tableData"]
    }

def gettabledata(post) -> dict:
    return {
      "_id": str(post["_id"]),
      "tableData": post["tableData"]
    }


def getuserLogo(post) -> dict:
    return {
        "id": str(post["_id"]),
        "profile": post["profile"],
        "title": post["title"]
    }

def getcurrentuserLogo(post) -> dict:
    return {
        "id": str(post["_id"]),
        "profile": post["profile"],
        "title": post["title"]
    }

def getmodulename(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "created_at": post["created_at"],
        "modulename": post["modulename"],
    }

