from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import FormtableDates
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import getmoduletabledata, gettabledata
from bson.objectid import ObjectId

router = APIRouter()


@router.post('/createtabledata')
async def create_tabledata(payload: schemas.tabledataSchema, user_id: str = Depends(oauth2.require_user)):
    payload.moduleId = payload.moduleId
    payload.recuriter = payload.recuriter
    payload.created_at = datetime.utcnow()
    payload.tableData = payload.tableData
    FormtableDates.insert_one(payload.dict())
    return {"status": "Form-tableData created successfully"}
    

@router.get('/moduletabledata/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    formtableDate = FormtableDates.find({'moduleId' : str(id) } )
    formtableData = []
    for form in formtableDate:
        formtableData.append(getmoduletabledata(form))
    return {"status": "success", "data": formtableData}

@router.get('/gettabledata/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    formtableDate = FormtableDates.find({'_id': ObjectId(id) } )
    formtableData = []
    for form in formtableDate:
        formtableData.append(gettabledata(form))
    return {"status": "success", "data": formtableData}

@router.get('/alltabledata', status_code=status.HTTP_200_OK)
def get_me(user_id: str = Depends(oauth2.require_user)):
    formtables = FormtableDates.find()
    formtableDates = []
    for form in formtables:
        formtableDates.append(gettabledata(form))
    return {"status": "success", "user": formtableDates}

@router.put('/updatetabledata/{id}', status_code=status.HTTP_200_OK)
async def update_tabledata(id: str, payload: schemas.updatetabledataSchema, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_tabledata = FormtableDates.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)})
    if not update_tabledata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-tabledata updated successfully"}

@router.delete('/deletetabledata/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_tabledata(id: str,  user_id: str=Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    post = FormtableDates.find_one_and_delete({'_id': ObjectId(id)})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-tabledata deleted successfully"}
