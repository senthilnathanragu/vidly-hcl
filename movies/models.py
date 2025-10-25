from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):

    def __str__(self):
        return self.title
    
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    number_in_stock = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=6,decimal_places=2)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
