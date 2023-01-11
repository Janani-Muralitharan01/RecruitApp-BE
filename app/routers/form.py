from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Form, User
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import getmodulename, formListEntity, getuserformEntity
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

@router.post('/createforms')
async def create_form(payload: schemas.formsSchema, user_id: str = Depends(oauth2.require_user)):
    payload.modulename = payload.modulename
    payload.recuriter = payload.recuriter
    payload.moduleelements = payload.moduleelements
    Form.insert_one(payload.dict())
    return {'status': 'Form updated successfully'}


@router.get('/allforms', status_code=status.HTTP_200_OK)
def get_me(user_id: str = Depends(oauth2.require_user)):
    forms = Form.find()
    formData = []
    for form in forms:
        formData.append(getuserformEntity(form))
    return {"status": "success", "user": formData}

@router.get('/getmodule', status_code=status.HTTP_200_OK)
def get_me(user_id: str = Depends(oauth2.require_user)):
    forms = Form.find()
    formData = []
    for form in forms:
        formData.append(getmodulename(form))
    return {"status": "success", "user": formData}

@router.get('/getforms/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    forms = Form.find({'_id': ObjectId(id)})
    formData = []
    for form in forms:
        formData.append(getuserformEntity(form))
    return {"status": "success", "data": formData}


@router.put('/updateforms/{id}', status_code=status.HTTP_200_OK)
async def update_form(id: str, payload: schemas.updateformSchema, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_form = Form.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)})
    if not update_form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-updated successfully"}


@router.delete('/deleteforms/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_form(id: str,  user_id: str=Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    post = Form.find_one_and_delete({'_id': ObjectId(id)})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-deleted successfully"}
