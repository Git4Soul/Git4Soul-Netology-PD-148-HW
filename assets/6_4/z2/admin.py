from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_tags = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main'):
                    main_tags += 1
        if main_tags == 0:
            raise ValidationError('Укажите один основной раздел.')
        if main_tags > 1:
            raise ValidationError('Основным может быть только один раздел.')

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
