from .models import Category, Project, Offer
from modeltranslation.translator import TranslationOptions,register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Offer)
class OfferTranslationOptions(TranslationOptions):
    fields = ('message', )