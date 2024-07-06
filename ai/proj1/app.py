from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
import json
import os

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 연결 설정
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.movie_database
movie_collection = database.get_collection("movies")

# Pydantic 모델 정의
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object id")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, handler):
        field_schema = handler({})
        field_schema.update(type="string")
        return field_schema

class MovieModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    영화명: str
    개봉년도: str
    평점: str
    관객수: int
    장르: str
    상영시간: str
    출연진: list
    줄거리: str
    포스터: str
    리뷰: list
    등급: str
    긍정비율: int
    부정비율: int
    긍정워드클라우드: list
    부정워드클라우드: list

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, 'data.json')

async def load_data():
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        await movie_collection.insert_many(data)
    else:
        await movie_collection.insert_one(data)

@app.on_event("startup")
async def startup_event():
    # 데이터 로드 및 MongoDB에 저장
    await load_data()

@app.get("/movies", response_model=list[MovieModel])
async def get_movies():
    movies = []
    async for movie in movie_collection.find():
        movies.append(MovieModel(**movie))
    return movies

@app.get("/movie/{movie_id}", response_model=MovieModel)
async def get_movie(movie_id: str):
    movie = await movie_collection.find_one({"_id": PyObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieModel(**movie)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
