from django.contrib import admin
from .models import Comment, Categories, Genres, Title, Review


class GenreInLine(admin.TabularInline):
    model = Title.genre.through


class TitlesAdmin(admin.ModelAdmin):
    inlines = [GenreInLine, ]


admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Review)
admin.site.register(Comment)
