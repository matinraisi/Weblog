from django.urls import path
from . import views
app_name = "blog"


urlpatterns = [
    path('', views.Home  , name = "index" ),
    # path('posts/', views.Post_list , name = "Post_list"),
    path('posts/', views.PostListview.as_view() , name = "Post_list"),
    path('posts/<int:id>/', views.Post_detail , name = "Post_detail"),
    # path('posts/<pk>', views.PostDitailview.as_view() , name = "Post_detail"),
    path('ticket/', views.create_ticket , name = "create_ticket"),
]