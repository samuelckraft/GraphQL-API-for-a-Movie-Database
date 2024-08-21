import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, db
from models import Genre as GenreModel
from sqlalchemy.orm import Session

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)

    get_movies_by_genre = graphene.List(Movie, genre_id=graphene.Int(required=True))
    
    get_genre_by_movie = graphene.List(Genre, movie_id=graphene.Int(required=True))

    def resolve_movies(self, info):
        return db.session.execute(db.select(MovieModel)).scalars().all()
    
    def resolve_genres(self, info):
        return db.session.execute(db.select(GenreModel)).scalars().all()

    def resolve_get_movies_by_genre(self, info, genre_id):
        return db.session.execute(db.select(MovieModel).filter(MovieModel.genre == genre_id)).scalars().all()
    
    def resolve_get_genre_by_movie(self, info, movie_id):
        genre_id = db.session.execute(db.select(MovieModel.genre).filter(MovieModel.id == movie_id)).scalar_one_or_none()
        
        if genre_id:
            return db.session.execute(db.select(GenreModel).filter(GenreModel.id == genre_id)).scalars().all()
        return []
    
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre = graphene.Int(required=True)

    product = graphene.Field(Movie)

    def mutate(self, info, title, director, year, genre):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, director=director, year=year, genre=genre)
                session.add(movie)
            
            session.refresh(movie)
            return AddMovie(movie=movie)


class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = GenreModel(name=name)
                session.add(genre)
            
            session.refresh(genre)
            return AddGenre(genre=genre)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year, genre):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel). where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year
                    movie.genre = genre

                else:
                    return None
            session.refresh(movie)
            return UpdateMovie(movie=movie)


class UpdateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel). where(GenreModel.id == id)).scalars().first()
                if genre:
                    genre.name = name

                else:
                    return None
            session.refresh(genre)
            return UpdateGenre(genre=genre)


class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel). where(MovieModel.id == id)).scalars().first()
                if movie:
                    session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)
        
class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    genre = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel). where(GenreModel.id == id)).scalars().first()
                if genre:
                    session.delete(genre)
                else:
                    return None
            session.refresh(genre)
            return DeleteGenre(genre=genre)
        

class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()

    create_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()