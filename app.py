from flask import Flask, jsonify
from flask_graphql import GraphQLView
import graphene
from schema import Query, Mutation
from models import db
from password import password


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost/movie_db'
db.init_app(app)

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/get_genre_by_movie', methods=['GET'])
def get_genre():
    genres = Query.resolve_get_genre_by_movie(None, info=None)
    return jsonify(genres)

@app.route('/get_movies_by_genre', methods=['GET'])
def get_movies():
    movies = Query.resolve_get_movies_by_genre(None, info=None)
    return jsonify(movies)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
