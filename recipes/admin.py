from django.contrib import admin
from .models import Recipe, Category



# Register your models here.

admin.site.site_header = "RecipeHub Admin"

admin.site.index_title = "Welcome To RecipeHub control panel"
admin.site.site_title = "Admin Panel"

# to approve the recipes
@admin.action(description="Approve")
def approve_recipe(ModelAdmin, request, queryset):
    queryset.update(approved = True)




# admin.site.register(Recipe)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    search_fields = ['title', 'description']
    
    list_filter = ('created_at','approved')
    list_display_links = ['id', 'title']
    readonly_fields = ['created_at', 'slug']
    fieldsets = (("Recipe Info",{"fields":['title', 'description', 'slug']}),
                 ("Preparation Info", {"fields":['ingredients','instructions']}),
                 ("Image", {"fields":['image']}),
                 ("Category", {"fields":['category']}),
                 ('Approve', {'fields':['approved']})
                 )
    actions = [approve_recipe]

    

admin.site.register(Category)

