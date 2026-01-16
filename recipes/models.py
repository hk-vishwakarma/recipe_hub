from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    approved = models.BooleanField(default=False)
    


    def save(self, *args, **kwargs):
        # Save first to get the ID if the object is new
        # if not self.id:
        #     super().save(*args, **kwargs)
        # Generate slug with title + ID
        self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class Feedback(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="feedbacks")
    # Optional: if you have user authentication
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)  # if no user system
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.recipe.title}"

