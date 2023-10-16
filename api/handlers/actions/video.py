from api.schemas.schemas import VideoCreate, ShowVideo
from database.dals import VideoDAL


async def _upload_video(video: VideoCreate, session) -> ShowVideo:
    async with session.begin():
        video_dal = VideoDAL(session)
        video = await video_dal.upload_video(
            name=video.name,
            file_path=video.file_path
        )
        return ShowVideo(
            video_id=video.video_id,
            name=video.name,
            file_path=video.file_path
        )

async def _get_video_by_id(video_id, session):
    async with session.begin():
        video_dal = VideoDAL(session)
        video = await video_dal.get_video_by_id(video_id=video_id)
        if video is not None:
            return video
