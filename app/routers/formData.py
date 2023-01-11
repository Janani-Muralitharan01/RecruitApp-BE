from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import FormDates
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import getmodulename
from bson.objectid import ObjectId

router = APIRouter()

@router.post('/createformvalue', status_code=status.HTTP_200_OK)
async def post_formvalue(payload: schemas.formvalueSchema, user_id: str = Depends(oauth2.require_user)):
    payload.moduleelements = payload.moduleelements
    FormDates.insert_one(payload.dict())
    return {'status' : 'Formvalue created successfully' }

@router.put('/updateformvalue/{id}', status_code=status.HTTP_200_OK)
async def update_formvalue(id: str, payload: schemas.formvalueSchema, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormValueId: {id}")
    update_formvalue = FormDates.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)})
    if not update_formvalue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Formvalue updated successfully"}

@router.delete('/deleteformvalue/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_formvalue(id: str,  user_id: str=Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    post = FormDates.find_one_and_delete({'_id': ObjectId(id)})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-deleted successfully"}
    
