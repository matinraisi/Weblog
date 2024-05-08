from django.urls import path
from . import views
app_name = "blog"


urlpatterns = [
    path('', views.Home  , name = "index" ),
    # path('posts/', views.Post_list , name = "Post_list"),
    path('posts/', views.PostListview.as_view() , name = "Post_list"),
    path('posts/<int:id>/', views.Post_detail , name = "Post_detail"),
    path('posts/<post_id>/comment', views.post_comments , name = "post_comments"),
    # path('posts/<pk>', views.PostDitailview.as_view() , name = "Post_detail"),
    path('ticket/', views.create_ticket , name = "create_ticket"),
    # path('posts/create/', views.crete_post , name = "crete_post"),
    path('posts/create/', views.crete_blog , name = "crete_blog"),
    path('posts/search/', views.post_search , name = "post_search"),
    path('profile/', views.profile , name = "profile"),
    path('profile/delete_post/<post_id>', views.delete_post , name = "delete_post"),
    path('profile/delete_image/<post_id>', views.delete_image , name = "delete_image"),
    path('profile/edit_post/<post_id>', views.edit_post , name = "edit_post"),

 


]