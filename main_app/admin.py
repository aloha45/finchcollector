from django.contrib import admin
from .models import Finch, Feeding, Seed

# Register your models here.
# class FeedingInline(admin.TabularInline):
#     model = Feeding
#     extra = 3

# class FinchAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['name', 'color', 'size', 'age']})
#     ]
#     inlines = [FeedingInline]

admin.site.register(Finch)
admin.site.register(Feeding)
admin.site.register(Seed)