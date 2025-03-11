from django.urls import path

from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("save-search",views.save_search,name="save-search"),
    path("tree",views.tree,name="tree"),
    path("save-history",views.save_history,name="save-history"),
    path("history",views.history,name="history"),
    path('history/specific_tree/<int:pk>/', views.history_detail, name='history_detail'),
    path('history/<int:pk>/', views.specific_tree, name='specific_tree'),
    path('history/<int:id>/delete/', views.delete_history, name='delete_history'),
    
]