from django.urls import path
from .views import *

app_name = 'recipes'

urlpatterns = [
    path('', home, name="home"),
    path("add-recipe/", create_recipe, name="create_recipe"),
    path('recipe_detail/<str:recipe_slug>/', recipe_detail,name="recipe_detail"),
    path('category/<str:category_slug>/', category_detail, name='category_detail'),
    path('categories/', category_list, name='category_list'),
    path('recipes/', all_recipes, name='all_recipes'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search_recipes, name='search_recipes'), 

    

]