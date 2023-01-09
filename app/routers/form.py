from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Form, User
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import formEntity, formListEntity, getuserformEntity
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

@router.post('/allforms')
async def create_form(payload: schemas.formsSchema):
    payload.formname = payload.formname
    payload.recuriter =payload.recuriter
    payload.formelements = payload.formelements
    Form.insert_one(payload.dict())
    return {'status' : 'Form updated successfully'}

@router.get('/getforms/{user_id}', status_code=status.HTTP_200_OK)
async def get_form(user_id: str,):
    forms = Form.find({'recuriter': user_id})
    formData =[]
    for form in forms:
        formData.append(getuserformEntity(form))
    return {"status": "success", "data":formData}



