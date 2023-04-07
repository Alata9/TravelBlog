from django.contrib import admin

from .forms import *
from .models import *


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
    form = SubRubricForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'image', 'is_active' )
    inlines = (AdditionalImageInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(Article, ArticleAdmin)


