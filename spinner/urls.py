from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/new/', views.create_list, name='create_list'),
    path('list/<int:list_id>/', views.list_detail, name='list_detail'),
    path('list/<int:list_id>/add/', views.add_item, name='add_item'),
    path('list/<int:list_id>/spin/', views.spin, name='spin'),
    path('result/<int:item_id>/', views.spin_result, name='spin_result'),
    path('history/', views.history, name='history'),
]