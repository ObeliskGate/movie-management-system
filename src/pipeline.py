# from init import db
# from models import MovieInfo,ActorInfo
from src.init import db
from src.models import MovieInfo,ActorInfo

def movie_search_pipeline(form):
    query_params = {
            'movie_id': MovieInfo.movie_id.ilike(f'%{str(form.movie_id.data)}%') if form.movie_id.data else None,
            'movie_name': MovieInfo.movie_name.ilike(f'%{form.movie_name.data}%') if form.movie_name.data else None,
            'release_date': MovieInfo.release_date == form.release_date.data if form.release_date.data else None,
            'country': MovieInfo.country.ilike(f'%{form.country.data}%') if form.country.data else None,
            'movie_type': MovieInfo.type.ilike(f'%{form.type.data}%') if form.type.data else None,
            'year': MovieInfo.year == form.year.data if form.year.data else None,
        }
    query = MovieInfo.query.filter(*(param for param in query_params.values() if param is not None))
    results = query.all()
    return results

def movie_add_pipeline(form):
    new_movie = MovieInfo(
            movie_id=str(form.movie_id.data),
            movie_name=form.movie_name.data,
            release_date=form.release_date.data,
            country=form.country.data,
            type=form.type.data,
            year=form.release_date.data.year
        )
    db.session.add(new_movie)
    db.session.commit()

def actor_search_pipeline(form):
    actor_id = form.actor_id.data
    actor_name = form.actor_name.data
    gender = form.gender.data
    country = form.country.data

    # Query the database based on the form data
    query = ActorInfo.query
    if actor_id:
        query = query.filter(ActorInfo.actor_id.ilike(f'%{actor_id}%'))
    if actor_name:
        query = query.filter(ActorInfo.actor_name.ilike(f'%{actor_name}%'))
    if gender is not None:
        query = query.filter(ActorInfo.gender.ilike(f'%{gender}%'))
    if country:
        query = query.filter(ActorInfo.country.ilike(f'%{country}%'))
    results = query.all()
    return results

def actor_add_pipeline(form):
    new_actor = ActorInfo(
            actor_id=str(form.actor_id.data),
            actor_name=form.actor_name.data,
            gender=form.gender.data,
            country=form.country.data,
        )
    db.session.add(new_actor)
    db.session.commit()


