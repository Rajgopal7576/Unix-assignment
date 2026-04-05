from django.db import models


class SearchHistory(models.Model):
    city_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, blank=True)
    temperature = models.FloatField()
    weather_condition = models.CharField(max_length=100)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = 'Search Histories'

    def __str__(self):
        return f"{self.city_name} - {self.searched_at.strftime('%Y-%m-%d %H:%M')}"


class FavoriteCity(models.Model):
    city_name = models.CharField(max_length=100, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['city_name']
        verbose_name_plural = 'Favorite Cities'

    def __str__(self):
        return self.city_name
