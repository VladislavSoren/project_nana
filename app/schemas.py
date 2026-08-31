from pydantic import BaseModel, Field
    

# --- Схема для запроса от клиента (тело POST-запроса) ---
class CourseCreate(BaseModel):
    name: str = Field(..., example="Название курса")
    author: str = Field(..., example="Автор курса")
    duration: int = Field(..., example=120, description="Длительность в минутах")
    price: float = Field(..., example=4990.00, description="Стоимость")
    discount: int = Field(0, example=10, description="Скидка в процентах")

# --- Схема для ответа сервера ---
class CourseResponse(BaseModel):
    name: str
    author: str
    duration: int
    price: float
    discount: int

    model_config = {"from_attributes": True}

class VideoResponse(BaseModel):
    title: str
    author: str
    course_id: int
    file_path: str

    model_config = {"from_attributes": True}

#######
# User
#######
class UserCreate(BaseModel):
    login: str = Field(..., example="Логин")
    password: str = Field(..., example="Пароль")
    name: str = Field(None, example="Имя")
    surname: str = Field(None, example="Фамилия")

class UserResponse(BaseModel):
    login: str
    name: str | None
    surname: str | None

    model_config = {"from_attributes": True}
