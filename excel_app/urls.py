from django.urls import path
from . import views

urlpatterns = [
     path('', views.upload_file, name='upload_file'),
     path('details/', views.details_view, name='details')

]
