from django_filters import rest_framework as filters
from project.models import Project, FavoritesProject


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name'] 


class FavoriteFilter(filters.FilterSet):
    project_name = filters.CharFilter(field_name='project__name', lookup_expr='icontains')

    class Meta:
        model = FavoritesProject
        fields = ['project_name'] 