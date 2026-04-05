from django.contrib import admin
from .models import SearchHistory, FavoriteCity

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'country_code', 'temperature', 'weather_condition', 'searched_at']
    list_filter = ['country_code', 'weather_condition']
    search_fields = ['city_name']

@admin.register(FavoriteCity)
class FavoriteCityAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'added_at']
