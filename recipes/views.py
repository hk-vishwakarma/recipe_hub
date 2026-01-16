from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q





# Create your views here.

# home page
def home(request):
    categories = Category.objects.all()
    # featured_recipes = Recipe.objects.all()[:6]

    recipes = Recipe.objects.filter(approved = True).annotate(avg_rating=Avg('feedbacks__rating'))[:6]

    # Round to nearest integer (0.5+ goes up)
    for recipe in recipes:
        if recipe.avg_rating:
            recipe.avg_rating = round(recipe.avg_rating)
        else:
            recipe.avg_rating = 0

    return render(request, 'recipes/index.html', {
        'categories': categories,
        # 'featured_recipes': featured_recipes,
        'now': datetime.now(),
        'recipes' : recipes,
    })


def create_recipe(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id) if category_id else None
        image = request.FILES.get("image")
        
        
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            category=category,
            image=image,
            approved = True if request.user.is_superuser else False    
        )

        

        recipe_id = recipe.id
        if not request.user.is_superuser:
            send_mail(
                subject = "A new recipe is added",
                message = f"""
                A new  recipe is added to the web


                Recipe ID : {recipe_id}
                Recipe Title : {recipe.title}

                You can view it at: http://127.0.0.1:8000/recipes/{recipe_id}/R
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list = ["hkvishwakarma01@gmail.com"],

            )


            messages.info(request, """Thank you for sharing your racipe.
                          Your recipe is currently under review and will be approved by the admin shortly.""")  
        return redirect("recipes:create_recipe")  

    return render(request, "recipes/create_recipe.html", {"categories": categories,
                                                           'now': datetime.now(),})


# def recipe_detail(request, recipe_id):
#     recipe = Recipe.objects.get(id = recipe_id)
#     return render(request, "recipes/detail_recipe.html", context = {'recipe':recipe})


# chana, oil, maida = ["chana", "oil", "maida"]
def recipe_detail(request, recipe_slug):
    
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    # recipe = Recipe.objects.get(id = recipe_id)
    ingredients_list = recipe.ingredients.split(',')

    if request.method == "POST":
        name = request.POST.get("name")
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("feedback")
        Feedback.objects.create(recipe=recipe, name=name, rating=rating, comment=comment)
        return redirect('recipes:recipe_detail', recipe_slug=recipe.slug)

    feedbacks = recipe.feedbacks.all().order_by('-created_at')

    # average_rating = recipe.feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0
    # average_rating = recipe.annotate(avg_rating=Avg('feedbacks__rating'))
    # average_rating = recipe.avg_rating = round(recipe.avg_rating)  # round to nearest integer

    avg_rating = recipe.feedbacks.aggregate(Avg('rating'))['rating__avg']

    if avg_rating is None:
        avg_rating = 0  # No feedback yet


    

    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "ingredients_list": ingredients_list,
        "feedbacks": feedbacks,
        "avg_rating" : avg_rating
    })


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    recipes = Recipe.objects.filter(category=category, approved = True).annotate(avg_rating=Avg('feedbacks__rating'))

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/category_detail.html', {
        'category': category,
        'recipes': recipes,
        'page_obj':page_obj,
        'now': datetime.now(),
    })

# To show all the categories on one page.
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'recipes/category_list.html', {'categories': categories ,
                                                          'now': datetime.now(),})

def all_recipes(request):
    recipes = Recipe.objects.filter(approved = True).annotate(avg_rating=Avg('feedbacks__rating')).order_by('-id')
    
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

#   pre 1 2 3 4 5 next

    # paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    return render(request, 'recipes/all_recipes.html', {
        'page_obj': page_obj,
        'now': datetime.now(),
    })

def about(request):
    return render(request, 'recipes/about.html', {'now': datetime.now(),})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        # Send email 
        send_mail(
            subject=f"Contact Form: {name}",
            message=f"""
            {message}
            name : {name}
            My email : {email}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('recipes:contact')

    return render(request, 'recipes/contact.html', {'now': datetime.now(),})





def search_recipes(request):
    query = request.GET.get('q')
    recipes = []

    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).annotate(avg_rating=Avg('feedbacks__rating'))


        # Round to nearest integer (0.5+ goes up)

        for recipe in recipes:
            if recipe.avg_rating:
                recipe.avg_rating = round(recipe.avg_rating)
            else:
                recipe.avg_rating = 0

    return render(request, 'recipes/search_results.html', {
        'query': query,
        'recipes': recipes,
        'now': datetime.now(),
    })


