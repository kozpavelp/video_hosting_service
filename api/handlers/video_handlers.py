import os
from logging import getLogger
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database.session import get_db
from api.schemas.schemas import VideoCreate
from api.handlers.actions.upload import _upload_video

logger = getLogger(__name__)
video_router = APIRouter()


@video_router.post('/upload')
async def upload_video(
        video: UploadFile = File(),
        db: AsyncSession = Depends(get_db)
):
    formats = ['mp4', 'avi', 'mov']
    extension = video.filename.split('.')[-1].lower()
    if extension not in formats:
        raise HTTPException(status_code=400, detail='Unsupported video format')

    upload_dir = "upload_videos"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_name = video.filename
    counter = 1
    while os.path.exists(os.path.join(upload_dir, file_name)):
        base_name, ext = os.path.splitext(video.filename)
        file_name = f"{base_name}_{counter}{ext}"
        counter += 1

    with open(os.path.join(upload_dir, file_name), 'wb') as video_file:
        video_file.write(video.file.read())

    try:
        video_file = VideoCreate(
            name=file_name,
            file_path=f'{upload_dir}/{file_name}'
        )
        video = await _upload_video(video_file, db)
        return video.video_id
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

