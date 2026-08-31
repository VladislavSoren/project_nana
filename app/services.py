from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.crud import _delete_file, _store_video_file, build_video_file_response
from app.models import Course, Video, User
from app.uow import UnitOfWork


class CourseService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create_course(self, obj_in):
        try:
            with self.uow_factory() as uow:
                if uow.courses is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")
                course = Course(**obj_in.model_dump())
                uow.courses.add(course)
                uow.flush()
                uow.commit()
                uow.session.refresh(course)
                return course
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой курс уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )


    def get_course(self, course_name: str):
        with self.uow_factory() as uow:
            if uow.courses is None:
                raise RuntimeError("UoW не инициализирован")
            course = uow.courses.get_by_name(course_name)

            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Курс с таким названием не найден",
                )

            return course

    def get_last_courses(self, number: int):
        with self.uow_factory() as uow:
            if uow.courses is None:
                raise RuntimeError("UoW не инициализирован")
            courses = uow.courses.list_last(number)

            if not courses:
                raise HTTPException(
                    status_code=404,
                    detail="В базе НЕТ курсов",
                )

            names = [course.name for course in courses]
            return ", ".join(names)


class VideoService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create(self, title, author, course, file):
        try:
            with self.uow_factory() as uow:
                if uow.video is None or uow.courses is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                course_obj = uow.courses.get_by_name(course)
                if not course_obj:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Курс с таким названием не найден, поэтому создать видео нельзя",
                    )

                file_path = _store_video_file(file)

                video = Video(
                    title=title,
                    author=author,
                    file_path=file_path,
                    course_id=course_obj.id,
                )
                uow.video.add(video)
                uow.commit()
                uow.session.refresh(video)
                return video
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такое видео уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )

    def upload(self, video_name: str, file: UploadFile):
        try:
            with self.uow_factory() as uow:
                if uow.video is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                video = uow.video.get_by_title(video_name)
                if not video:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Видео с таким названием не найдено",
                    )

                old_file_path = video.file_path
                video.file_path = _store_video_file(file)

                uow.commit()
                uow.session.refresh(video)

            _delete_file(old_file_path)
            return video
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )

    def get(self, video_name: str) -> Video:
        with self.uow_factory() as uow:
            if uow.video is None:
                raise RuntimeError("UoW не инициализирован")
            video = uow.video.get_by_title(video_name)

            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Видео с таким названием не найдено",
                )

            return video

    def get_file(self, video_name: str, download: bool = False) -> FileResponse:
        video = self.get(video_name)
        return build_video_file_response(video, download=download)

    def get_last(self, number: int):
        with self.uow_factory() as uow:
            if uow.video is None:
                raise RuntimeError("UoW не инициализирован")
            videos = uow.video.list_last(number)

            if not videos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="В базе НЕТ видео",
                )

            titles = [video.title for video in videos]
            return ", ".join(titles)
        
class UserService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create(self, obj_in):
        try:
            with self.uow_factory() as uow:
                if uow.user is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                videos = uow.video.get_introductory()

                # Прописать получение названий видео
                videos_names = ...

                # Прописать передачу videos_names в User
                user = User(**obj_in.model_dump()) # Подправить эту строку
                uow.user.add(user)
                uow.commit()
                uow.session.refresh(user)
                return user
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой пользователь уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )