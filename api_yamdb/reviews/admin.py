from django.contrib import admin

from .models import Comment, Categories, Genres, Title, Review


admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
