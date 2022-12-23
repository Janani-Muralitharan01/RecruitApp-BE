from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Form, User
from app.oauth2 import require_user
from app.serializers.formSerializers import formEntity, formListEntity
from bson.objectid import ObjectId

router = APIRouter()

@router.get('/')
def get_forms(limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    forms = formListEntity(Form.aggregate(pipeline))
    return {'status': 'success', 'results': len(forms), 'forms': forms}
