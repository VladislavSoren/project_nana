from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, Video, User


class CourseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, course: Course) -> Course:
        self.session.add(course)
        return course

    def get_by_name(self, course_name: str) -> Course | None:
        stmt = select(Course).where(Course.name == course_name)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_last(self, number: int) -> list[Course]:
        return (
            self.session.query(Course)
            .order_by(Course.name)
            .limit(number)
            .all()
        )

    def get_all(self):
            stmt = select(Course)
            return self.session.execute(stmt).all()


class VideoRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, video: Video) -> Video:
        self.session.add(video)
        return video

    def get_by_title(self, title: str) -> Video | None:
        stmt = select(Video).where(Video.title == title)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_last(self, number: int) -> list[Video]:
        return (
            self.session.query(Video)
            .order_by(Video.title)
            .limit(number)
            .all()
        )

    def get_introductory(self):
        stmt = select(Video).where(...)  # здесь прописать условия поиска по слову "ознакомительное" 
        return self.session.execute(stmt).scalars()


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: User) -> User:
        self.session.add(obj)
        return obj

    def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalar_one_or_none()

