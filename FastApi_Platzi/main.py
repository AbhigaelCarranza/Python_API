#FastApi
from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import status
from fastapi.security import HTTPBearer

#Pydantic
from pydantic import BaseModel, Field

#Python
from typing import Optional, List
from jwt_manager import create_token, validate_token
from models.movie import Movie as MovieModel
from config.database import Session, engine, Base

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

#Models
##Token
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales son invalidas")

##User login
class User(BaseModel):
    email:str
    password:str

##Info Movie
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(
        min_length=5, 
        max_length=15
        )
    overview: str = Field(
        min_length=15, 
        max_length=50
        )
    year: int = Field(
        le=2022
        )
    rating:float = Field(
        ge=1, 
        le=10
        )
    category:str = Field(
        min_length=5, 
        max_length=15
        )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }


movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

#Path Operations
@app.get(
    path='/',
    tags=['home']
    )
def message():
    return HTMLResponse('<h1>Hello world</h1>')

##Login
@app.post(
    path='/login', 
    tags=['auth'],
    status_code=status.HTTP_200_OK
    )
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)

##Get all Movies
@app.get(
    path='/movies',
    tags=['movies'],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=status.HTTP_200_OK,content=movies)

##Get a Movie for id
@app.get(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=Movie,
    status_code=status.HTTP_200_OK
    )
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=status.HTTP_200_OK,content=item)
    return JSONResponse(content=[],status_code=status.HTTP_404_NOT_FOUND)

##Get all Movies for category
@app.get(
    path='/movies/', 
    tags=['movies'], 
    response_model=List[Movie],
    status_code=status.HTTP_200_OK
    )
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    return JSONResponse(status_code=status.HTTP_200_OK,content=data)

##Post a Movie
@app.post(
    path='/movies', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_201_CREATED
    )
def create_movie(movie: Movie) -> dict:
    db = Session()                          #se crea una session
    new_movie = MovieModel(**movie.dict()) #se pasan los parametros como un diccionario opcional kwargs, de la clase Movie
    db.add(new_movie)                       #se añade la pelicula nueva a la base de datos
    db.commit() #Se actualiza la tabla
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"message": "Se ha registrado la película"})

##Update a Movie
@app.put(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_200_OK
    )
def update_movie(id: int, movie: Movie)-> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=status.HTTP_200_OK,content={"message": "Se ha modificado la película"})

##Delete
@app.delete(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_200_OK
    )
def delete_movie(id: int)-> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message": "Se ha eliminado la película"})