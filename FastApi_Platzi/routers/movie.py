from fastapi import APIRouter,status
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

##Get all Movies
@movie_router.get(
    path='/movies',
    tags=['movies'],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()  #Se especifica la tabla a la cual se quiere consultar
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

##Get a Movie for id
@movie_router.get(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=Movie,
    status_code=status.HTTP_200_OK
    )
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

##Get all Movies for category
@movie_router.get(
    path='/movies/', 
    tags=['movies'], 
    response_model=List[Movie],
    status_code=status.HTTP_200_OK
    )
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

##Post a Movie
@movie_router.post(
    path='/movies', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_201_CREATED
    )
def create_movie(movie: Movie) -> dict:
    db = Session()                          
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"message": "Se ha registrado la película"})

##Update a Movie
@movie_router.put(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_200_OK
    )
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

##Delete
@movie_router.delete(
    path='/movies/{id}', 
    tags=['movies'], 
    response_model=dict,
    status_code=status.HTTP_200_OK
    )
def delete_movie(id: int)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})