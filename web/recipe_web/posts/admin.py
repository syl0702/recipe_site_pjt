from django.contrib import admin

# Register your models here.
from .models import Post, Ingred, RecipeIngred, RecipeDetail,Rating
# Register your models here.

admin.site.register(Post)
admin.site.register(Ingred)
admin.site.register(RecipeIngred)
admin.site.register(RecipeDetail)
admin.site.register(Rating)
