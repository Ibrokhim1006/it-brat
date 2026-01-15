from django.urls import path
from project.views import (
    ProjectCategoryView,
    ProjectCategoryGetView,
    ProjectsView,
    ProjectView,
    FavoritesProjectView,
    FavoriteProjectView,
    NotificationsView,
    NotificationView,
    NotificationCountView,
)


urlpatterns = [
    path('category/project/', ProjectCategoryView.as_view()),
    path('category/<int:pk>/project/', ProjectCategoryGetView.as_view()),
    path('project/', ProjectsView.as_view()),
    path('project/<int:pk>/', ProjectView.as_view()),
    # Favorite project
    path('fovorite/project/', FavoritesProjectView.as_view()),
    path('favorite/project/<int:pk>/', FavoriteProjectView.as_view()),
    # Notfiation
    path('project/notification/', NotificationsView.as_view()),
    path('project/notification/<int:pk>/', NotificationView.as_view()),
    path('project/notification/count/', NotificationCountView.as_view()),

]