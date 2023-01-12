from datetime import datetime, timedelta
import hashlib
from io import BytesIO
from random import randbytes
from bson.objectid import ObjectId
from fastapi import APIRouter, Form, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr
from fastapi import FastAPI, File, UploadFile
from app import oauth2
from app.database import UserLogos
from app.email import Email
from fastapi import FastAPI, File, UploadFile
from app.serializers.formSerializers import getuserLogo
from .. import schemas, utils
from app.oauth2 import AuthJWT
from ..config import settings

router = APIRouter()


@router.post('/createlogo', status_code=status.HTTP_201_CREATED)
async def create_logo(profile: UploadFile, tittle: str = Form(), user_id: str = Depends(oauth2.require_user)):
    images = UserLogos.insert_one({"profile": profile.filename, "tittle": tittle})
    logoDetails = UserLogos.find_one({'_id': images.inserted_id})
    imageDetails = []
    imageDetails.append(getuserLogo(logoDetails))
    return {"status": "Profile-image and tittle created successfully", "data": imageDetails}

@router.get('/getuserlogo/{id}',status_code=status.HTTP_200_OK)
async def get_logos(id: str,):
     if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
     logos = UserLogos.find({'_id': ObjectId(id)})
     userlogoData = []
     for logo in logos:
        userlogoData.append(getuserLogo(logo))
     return {"status": "success", "data": userlogoData} 

@router.put('/updatelogo/{id}', status_code=status.HTTP_200_OK)
async def update_logo(id: str, profile: UploadFile, tittle: str = Form(),  user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_logo = UserLogos.find_one_and_update({'_id': ObjectId(id)}, {'$set': {"profile": profile.filename, "tittle": tittle }})
    if not update_logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "User-logo and tittle updated successfully"}

@router.delete('/deletelogo/{id}', status_code=status.HTTP_200_OK)
async def delete_logo(id: str,  user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    delete_logo = UserLogos.find_one_and_delete({'_id': ObjectId(id)})
    if not delete_logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "User-logo and tittle deleted successfully"}
