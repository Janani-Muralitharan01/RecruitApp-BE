from datetime import datetime, timedelta
import hashlib
from io import BytesIO
import boto3
from random import randbytes
from bson.objectid import ObjectId
from fastapi import APIRouter, Form, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr
from fastapi import FastAPI, File, UploadFile
from app import oauth2
from app.database import UserLogos
from app.email import Email
from app.serializers.formSerializers import getuserLogo,getcurrentuserLogo
from .. import schemas, utils
from app.oauth2 import AuthJWT
from ..config import settings
from botocore.client import BaseClient
from fastapi.responses import JSONResponse
from app.setting import s3_auth
from app.upload import upload_file_to_bucket

router = APIRouter()




@router.post('/createlogo', status_code=status.HTTP_201_CREATED)
async def upload_file( s3: BaseClient = Depends(s3_auth), profile: UploadFile = File(...), title: str = Form()):
    now = datetime.now()
    created_at= datetime.now(),
    upload_obj = upload_file_to_bucket(s3_client=s3, profile=profile.file,
                                       bucket='userlogoimage',
                                       object_name=profile.filename
                                       )
    if upload_obj:
        image = f'https://userlogoimage.s3.amazonaws.com/{profile.filename}'
        result = UserLogos.insert_one({"profile": image, "title": title, "created_at": created_at})
        logoDetails = UserLogos.find_one({'_id': result.inserted_id})
        imageDetails = []
        imageDetails.append(getuserLogo(logoDetails))
        return {"status": "Profile-image and tittle created successfully", "data": imageDetails}
            
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")


@router.get('/currentuserlogo', status_code=status.HTTP_200_OK)
async def get_currentlogo():
    logos = UserLogos.find().sort('created_at', -1).limit(1)
    userlogoData = []
    for logo in logos:
         userlogoData.append(getcurrentuserLogo(logo))
   
    return {"data":userlogoData }

@router.get('/getuserlogo/{id}', status_code=status.HTTP_200_OK)
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
async def update_logo(id: str, profile: UploadFile, title: str = Form(),  user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_logo = UserLogos.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': {"profile": profile.filename, "tittle": title}})
    if not update_logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "User-logo and tittle updated successfully"}


@router.delete('/deletelogo/{id}', status_code=status.HTTP_200_OK)
async def delete_logo(id: str, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    delete_logo = UserLogos.find_one_and_delete({'_id': ObjectId(id)})
    if not delete_logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "User-logo and tittle deleted successfully"}
