from django.urls import path, include
from rest_framework import routers

from . import views
from .views import BookList, SearchResultView


router = routers.DefaultRouter()
router.register('books', views.BookView)


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('add/', views.add, name='add'),
    path('show/', SearchResultView.as_view(), name='show'),
    path('book_list/', BookList.as_view(), name='list'),
    path('update/<str:pk>/', views.update, name='update'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('api_import/', views.api_import, name='api_import')
    ]
