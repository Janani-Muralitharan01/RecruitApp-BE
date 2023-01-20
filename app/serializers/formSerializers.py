import datetime
from app.serializers.userSerializers import embeddedUserResponse


def formEntity(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "category": post["category"],
        "content": post["content"],
        "image": post["image"],
        "user": str(post["user"]),
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }


def populatedformEntity(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "category": post["category"],
        "content": post["content"],
        "image": post["image"],
        "user": embeddedUserResponse(post["user"]),
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }


def getuserformEntity(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "modulename": post["modulename"],
        "recuriter": post['recuriter'],
        "moduleelements": post["moduleelements"],
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
        "tableData": post["tableData"]
    }

def formListEntity(forms) -> list:
    return [populatedformEntity(form) for form in forms]
