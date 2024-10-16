from django.shortcuts import render,redirect
from recipe.models import *
# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(status='Approved',is_approved=True).order_by('?')[:3]
    hot_recipes = Recipe.objects.filter(status='Approved',is_approved=True).order_by('?')[:4]
    recipes_of_the_day = Recipe.objects.filter(status='Approved',is_approved=True).order_by('?')[:1]
    return render(request,'website/home.html',{'recipes':recipes,'hot_recipes':hot_recipes,'recipes_of_the_day':recipes_of_the_day})