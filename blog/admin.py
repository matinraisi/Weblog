from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
# Register your models here.
# admin.sites.AdminSite.site_header = " پنل مدیریتی جنگو"
# admin.sites.AdminSite.site_title = "پنل"
# admin.sites.AdminSite.index_title = "پنل مدیریتی"
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' , 'author' , 'publish','status']
    ordering = ['title','publish']
    list_filter = ['status',('publish' ,JDateFieldListFilter)]
    search_fields = ['title' , 'description' ]
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug":['title']}
    list_editable = ['status']
    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['name' , 'email' , 'phone' , 'sunject']
    ordering = ['name']
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name' , 'post' , 'created','active']
    list_filter = ['active',('created' ,JDateFieldListFilter) , ('updated' ,JDateFieldListFilter)]
    search_fields = ['name' , 'body' ]
    list_editable = ['active']
    