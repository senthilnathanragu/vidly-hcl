from django.db import models
from tastypie.resources import ModelResource
from movies.models import Movie
# movie/views.py





# Create your models here.
class MovieResource(ModelResource):
    class Meta:
        # defines some meta data about our movie resource
        queryset = Movie.objects.all()
        # it will provide a query that going to be executed somewhere in the future, thats why it is called as lazyloading
        resource_name = "movies"  # api will be available at 'api/movies'
        excludes = ["release_year"]
