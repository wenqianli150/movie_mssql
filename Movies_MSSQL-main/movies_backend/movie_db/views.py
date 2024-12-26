import requests
from django.db import connection
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def query(request):
    """
    This function queries the database for movies, filtering
    by the criteria present in the request

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """

    actor = request.query_params.get('actor')
    genre = request.query_params.get('genre')
    rating = request.query_params.get('rating')

    print(actor, genre, rating)

    sql_query = f"select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                  from MOVIE as m \
                  join MOVIE_CAST as c on m.movie_id = c.movie_id \
                  join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                  join RATING as r on mr.rating_id = r.rating_id \
                  group by m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type"

    if actor and actor != "NONE":
        sql_query = sql_query + f" intersect \
                    select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                    from MOVIE as m \
                    join MOVIE_CAST as c on m.movie_id = c.movie_id \
                    join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                    join RATING as r on mr.rating_id = r.rating_id \
                    join ACTOR as a on c.actor_id = a.actor_id \
                    where a.actor_name = '{actor}'"

    if genre and genre != "NONE":
         sql_query = sql_query + f" intersect \
                    select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                    from MOVIE as m \
                    join MOVIE_GENRE as mg on m.movie_id = mg.movie_id \
                    join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                    join RATING as r on mr.rating_id = r.rating_id \
                    join GENRE as g on mg.genre_id = g.genre_id \
                    where g.genre_name = '{genre}'"

    if rating and rating != "NONE":
        sql_query = sql_query + f" intersect \
                    select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                    from MOVIE as m \
                    join MOVIE_GENRE as mg on m.movie_id = mg.movie_id \
                    join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                    join RATING as r on mr.rating_id = r.rating_id \
                    where r.rating_type = '{rating}'"         

   
    sql_query = sql_query + " order by m.movie_title"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchall()


    return JsonResponse(row, safe=False)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def get_favorites(request):
    """
    This function queries the database for favorited movies
    Only information about movies that have been favorited is returned
    

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """

    sql_query = f"select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                  from MOVIE as m \
                  join MOVIE_CAST as c on m.movie_id = c.movie_id \
                  join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                  join RATING as r on mr.rating_id = r.rating_id \
                  where m.favorite > 0 \
                  group by m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type"        

   
    sql_query = sql_query + " order by m.movie_title"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchall()


    return JsonResponse(row, safe=False)


@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def unfavorite_movie(request):
    """
    This function sets the value of the movie's favorite column to 0.
    The movie is determined by the movie id provided to this function

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """
    mid = request.query_params.get('id')
    if not mid:
        return JsonResponse('Provide movie_id as \'id\' parameter', status=status.HTTP_400_BAD_REQUEST, safe=False)

    sql_query = f'select m.movie_title from MOVIE as m where m.movie_id = {mid}'
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        title = cursor.fetchall()

    if title == []:
        return JsonResponse(f'Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

    sql_query = f'update MOVIE set favorite = 0 where movie_id = {mid}'
    with connection.cursor() as cursor:
        cursor.execute(sql_query)

    return JsonResponse(f'Record Updated Successfully!', status=status.HTTP_200_OK, safe=False)


@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def favorite_movie(request):
    """
    This function sets the value of the movie's favorite column to 1.
    The movie is determined by the movie id provided to this function

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """
    mid = request.query_params.get('id')
    if not mid:
        return JsonResponse('Provide movie_id as \'id\' parameter', status=status.HTTP_400_BAD_REQUEST, safe=False)

    sql_query = f'select m.movie_title from MOVIE as m where m.movie_id = {mid}'
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        title = cursor.fetchall()

    if title == []:
        return JsonResponse(f'Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

    sql_query = f'update MOVIE set favorite = 1 where movie_id = {mid}'
    with connection.cursor() as cursor:
        cursor.execute(sql_query)

    sql_query = f"select m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type \
                  from MOVIE as m \
                  join MOVIE_CAST as c on m.movie_id = c.movie_id \
                  join MOVIE_RATING as mr on m.movie_id = mr.movie_id \
                  join RATING as r on mr.rating_id = r.rating_id \
                  where m.movie_id = {mid} \
                  group by m.movie_id, m.movie_title, m.movie_country, m.movie_duration, m.movie_year, r.rating_type"
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        response = cursor.fetchall()[0]

    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def get_actors(request):
    """
    This function gets all of the actors in the db

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """

    sql_query = f"select distinct actor_name from ACTOR order by actor_name"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchall()


    return JsonResponse(row, safe=False)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def get_genres(request):
    """
    This function gets all of the genres in the db

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """

    sql_query = f"select distinct genre_name from GENRE order by genre_name"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchall()


    return JsonResponse(row, safe=False)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def get_ratings(request):
    """
    This function gets all of the ratings in the db

    Args:
        request (HttpRequest): An http request.

    Returns:
        [JsonResponse]: A json response with data array
    """

    sql_query = f"select distinct rating_type from RATING order by rating_type"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchall()


    return JsonResponse(row, safe=False)