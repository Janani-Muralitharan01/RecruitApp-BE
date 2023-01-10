from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Form, FormDates
from typing import Union
from app.oauth2 import require_user
from app import oauth2
from app.serializers.formSerializers import getmodulename
from bson.objectid import ObjectId

router = APIRouter()

@router.put('/updateformvalue/{id}', status_code=status.HTTP_200_OK)
async def update_formvalue(id: str, payload: schemas.formvalueSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_form = FormDates.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)})
    if not update_form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Formvalue-updated successfully"}
