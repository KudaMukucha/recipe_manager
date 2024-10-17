from django.db import IntegrityError
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
def create_recipe(request):
    if not request.user.is_chef:
        return HttpResponseForbidden('You are not allowed to access this page. Register as a chef first!')
    
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, request.FILES)  # handle files for image upload

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.chef = request.user
            recipe.save()
            messages.success(request,'Recipe submitted successfully. Your recipe is now under review.')
            return redirect('recipe:chef-recipes')
        else:
            messages.warning(request, 'Oops, something went wrong.')
            return redirect('recipe:create-recipe')

    else:
        form = CreateRecipeForm()
        return render(request, 'recipe/submit-recipe.html', {'form': form})

def chef_recipes(request):
    recipe_list = Recipe.objects.filter(chef = request.user).order_by('-created')
    paginator = Paginator(recipe_list,5)
    page_number = request.GET.get('page',1)
    try:
        recipes = paginator.page(page_number)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    return render(request,'recipe/chef-recipes.html',{'recipes':recipes})

def admin_recipes(request):
    if request.user.is_admin:
        recipe_list = Recipe.objects.filter(status='Pending',is_approved=False).order_by('created')
        paginator = Paginator(recipe_list,5)
        page_number = request.GET.get('page',1)
        try:
            recipes = paginator.page(page_number)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            recipes = paginator.page(1)
    return render(request,'recipe/review-recipes.html',{'recipes':recipes})

def site_recipes(request):
    recipe_list = Recipe.objects.filter(status='Approved',is_approved=True).order_by('?')
    paginator = Paginator(recipe_list,5)
    page_number = request.GET.get('page',1)
    try:
        recipes = paginator.page(page_number)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    return render(request,'recipe/site-recipes.html',{'recipes':recipes})

def recipe_details(request,slug):
    recipe = Recipe.objects.get(slug=slug)
    ingredients = recipe.ingredients.split(',')
    comments = recipe.comments.filter(active=True)
    form = CreateCommentForm()
    related_recipes = Recipe.objects.filter(category = recipe.category).exclude(pk=recipe.pk).filter(status='Approved',is_approved=True).order_by('?')[:3]
    return render(request,'recipe/recipe-details.html',{'recipe':recipe,'ingredients':ingredients,'form':form,'comments':comments,'related_recipes':related_recipes})

def post_comment(request,pk):
    recipe = Recipe.objects.get(pk=pk)
    comment = None
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            return render(request,'recipe/comment.html',{'form':form,'comment':comment,'recipe':recipe})
        
def resolve_recipe(request,pk):
    recipe = Recipe.objects.get(pk = pk)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        action = request.POST.get('action')
        if action == 'approve':
            recipe.admin_reply = reply
            recipe.is_approved = True
            recipe.status = 'Approved'
            messages.success(request,'Recipe approved..')
        elif action == 'decline':
            recipe.admin_reply = reply
            recipe.is_approved = False
            recipe.status = 'Declined'
            messages.success(request,'Recipe rejected..')
    recipe.save()
    return redirect('recipe:review-recipes')

def update_recipe(request,pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateRecipeForm(request.POST,request.FILES,instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.status = 'Pending'
            recipe.is_approved = False
            recipe.save()
            messages.success(request,'Recipe updated successfully. Hang tight while the adminstrator is reviewing it.')
            return redirect('recipe:chef-recipes')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again')
            return redirect('recipe:update-recipe')
    else:
        form = UpdateRecipeForm(instance=recipe)
        return render(request,'recipe/update-recipe.html',{'form':form})
    
def recipes_per_category(request,category_name):
    category = Category.objects.get(name__iexact = category_name)
    recipe_list = Recipe.objects.filter(category=category,status='Approved',is_approved=True)
    paginator = Paginator(recipe_list,5)
    page_number = request.GET.get('page',1)
    try:
        recipes = paginator.page(page_number)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        recipes = paginator.page(1)

    return render(request,'recipe/category-recipes.html',{'recipes':recipes,'category':category})

def search_recipes(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(status='Approved',is_approved=True)

    if query:
        recipes = recipes.filter(
            Q(title__icontains = query) |
            Q(description__icontains=query)|
            Q(cuisine__icontains=query) |
            Q(course__icontains=query)
        )
    
    paginator = Paginator(recipes,5)
    page_number = request.GET.get('page',1)
    try:
        recipes = paginator.page(page_number)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    page_number = request.GET.get('page',1)
    return render(request,'recipe/search-results.html',{'recipes':recipes,'query':query})


    
