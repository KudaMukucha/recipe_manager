from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns =[
    path('submit-recipe/',views.create_recipe,name='create-recipe'),
    path('my-recipes/',views.chef_recipes,name='chef-recipes'),
    path('review-recipes/',views.admin_recipes,name='review-recipes'),
    path('recipes/',views.site_recipes,name='site-recipes'),
    path('recipe-details/<str:title>/',views.recipe_details,name='recipe-details'),
    path('comment/<int:pk>/',views.post_comment,name='post-comment'),
    path('resolve-recipe/<int:pk>/',views.resolve_recipe,name='resolve-recipe'),
    path('update-recipe/<int:pk>/',views.update_recipe,name='update-recipe'),
    path('category/<str:category_name>/',views.recipes_per_category,name='recipes-per-category'),
    path('search/',views.search_recipes,name='search-recipes')
]