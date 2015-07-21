from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created')


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 1


class SPAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'category')
    list_filter = ['category']
    inlines = [ReviewInLine]

class CityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__')

admin.site.register(SP, SPAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(City)
admin.site.register(Street)