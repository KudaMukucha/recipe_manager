from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    STATUS_CHOICES =[
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Pending','Pending')
    ]
    SKILL_LEVEL_CHOICES =[
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Advanced','Advanced')
    ]
    COURSE_CHOICES =[
        ('main_course','Main Course'),
        ('side_dish','Side Dish'),
        ('desert','Desert'),
        ('snack','Snack')

    ]

    CUISINE_CHOICES =[
        ('Italian','Italian'),
        ('French','French'),
        ('Chinese','Chinese'),
        ('Indian','Indian'),
        ('Mexican','Mexican')
    ]
    chef = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='chef_recipes')
    approver = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='approver_recipes',null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='recipes',null=True,blank=True)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    ready_in = models.IntegerField()
    servings = models.IntegerField()
    recipe_yield = models.IntegerField()
    skill_level = models.CharField(max_length=20,choices=SKILL_LEVEL_CHOICES,default='Medium')
    video_link = models.CharField(max_length=100)
    calories = models.CharField(max_length=15)
    carbohydrates = models.CharField(max_length=15)
    fat = models.CharField(max_length=15)
    protein = models.CharField(max_length=15)
    cholestrol = models.CharField(max_length=15)
    dietary_fiber = models.CharField(max_length=15)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_recipes')
    course = models.CharField(max_length=20,choices=COURSE_CHOICES,default='main_course')
    cuisine = models.CharField(max_length=20,choices=CUISINE_CHOICES,default='Italian')
    ingredients = models.TextField()
    steps = models.TextField()
    admin_reply = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.recipe}'
        


