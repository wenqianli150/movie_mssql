from django.urls import include, path

from . import views

urlpatterns = [
    path(r'api/query', views.query),
    path(r'api/favorites', views.get_favorites),
    path(r'api/favorite_movie', views.favorite_movie),
    path(r'api/unfavorite_movie', views.unfavorite_movie),
    path(r'api/actors', views.get_actors),
    path(r'api/genres', views.get_genres),
    path(r'api/ratings', views.get_ratings),
    path(r'api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
