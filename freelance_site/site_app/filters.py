from django_filters import FilterSet
from .models import Project


class ProjectFilter(FilterSet):
    class Meta:
        model = Project
        fields = {
            'title': ['exact'],
            'description': ['exact'],
            'category': ['exact'],
            'budget': ['gt', 'lt'],
            'skills_required': ['exact']
        }