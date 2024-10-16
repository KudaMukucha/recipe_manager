from django import forms
from .models import Recipe,Comment

class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude =['chef','approver','status','created','updated','is_approved','rating','rating_count','recipe_of_the_day']

class UpdateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude =['chef','approver','status','created','updated','is_approved','rating','rating_count','recipe_of_the_day']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']

        

