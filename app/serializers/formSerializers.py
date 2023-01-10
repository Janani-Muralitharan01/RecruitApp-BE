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
        "moduleelements": post["moduleelements"]
    }

def getmodulename(post) -> dict: 

    return{
         "_id": str(post["_id"]),
        "modulename": post["modulename"],
    }


def formListEntity(forms) -> list:
    return [populatedformEntity(form) for form in forms]


