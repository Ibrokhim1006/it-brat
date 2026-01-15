from django_filters import rest_framework as filters
from resume.models import ResumeModel, FavoritesResume
from django.db.models import Q


class ResumetFilter(filters.FilterSet):
    resume_owner = filters.CharFilter(method='filter_by_full_name')

    class Meta:
        model = ResumeModel
        fields = ['resume_owner'] 
    
    def filter_by_full_name(self, queryset, name, value):
        # Filter by owner's first name or last name
        return queryset.filter(
            Q(owner__first_name__icontains=value) |
            Q(owner__last_name__icontains=value)
        )


class FavoriteFilter(filters.FilterSet):
    resume_owner = filters.CharFilter(method='filter_by_full_name')

    class Meta:
        model = FavoritesResume
        fields = ['resume_owner'] 
    
    def filter_by_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(resume__owner__first_name__icontains=value) |
            Q(resume__owner__last_name__icontains=value)
        )