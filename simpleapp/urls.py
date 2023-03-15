from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    path('', NewsList.as_view(), name='allnews'),
    path('<int:pk>', NewsDetail.as_view(), name='post'),
]