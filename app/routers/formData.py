from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import FormtableDates
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import gettabledata
from bson.objectid import ObjectId

router = APIRouter()


@router.post('/createtabledata')
async def create_tabledata(payload: schemas.tabledataSchema, user_id: str = Depends(oauth2.require_user)):
    payload.recuriter = payload.recuriter
    payload.created_at = datetime.utcnow()
    payload.tableData = payload.tableData
    FormtableDates.insert_one(payload.dict())
    return {"status": "Form-tableData created successfully"}
    

@router.get('/gettabledata/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    formtableDates = FormtableDates.find({'_id': ObjectId(id)})
    formtableData = []
    for form in formtableDates:
        formtableData.append(gettabledata(form))
    return {"status": "success", "data": formtableData}

@router.get('/alltabledata', status_code=status.HTTP_200_OK)
def get_me(user_id: str = Depends(oauth2.require_user)):
    formtables = FormtableDates.find()
    formtableDates = []
    for form in formtables:
        formtableDates.append(gettabledata(form))
    return {"status": "success", "user": formtableDates}
