from django.contrib import admin
from .models import Category, State, Region, Company, Type, Tag, Contact
# Register your models here.

admin.site.register(Category),
admin.site.register(Tag),
admin.site.register(Type),
admin.site.register(Contact),


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class RegionAdmin(admin.TabularInline):
    model = Region
    extra = 1


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = (RegionAdmin, )
    list_display = ('id', 'title')
