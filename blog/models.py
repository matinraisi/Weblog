from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
# Create your models here.
class publishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISH)
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF' ,'Draft'
        PUBLISH = 'PB' , 'Publish'
        REJECTED = 'RJ' , 'Rejected'
        
    author = models.ForeignKey(User , on_delete = models.CASCADE,related_name = "user_posts" ,verbose_name = "نویسنده")
    title = models.CharField(max_length =100 ,verbose_name = "عنوان" )
    description = models.TextField(verbose_name = "توضیحات")
    slug = models.SlugField(max_length =100)
    # time 
    publish = jmodels.jDateTimeField(default=timezone.now,verbose_name = "تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True,verbose_name = "تاریخ ساخت")
    updated = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length =10 , choices = Status.choices , default = Status.DRAFT,verbose_name = "وضعیت")

    # objects = models.Manager()
    objects = jmodels.jManager()
    published = publishedManager()
    class Meta:
        ordering = ['-publish']
        # for search index in table 
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        
        
    def __str__(self) :
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:Post_detail", kwargs={"id": self.id})



class Ticket(models.Model):
    name = models.CharField(max_length =50  ,verbose_name = "نام فرستند")
    massege = models.TextField(verbose_name = "پیام")
    email = models.EmailField(verbose_name = "ایمیل")
    phone = models.CharField(max_length =11 , verbose_name = "تلفن همراه" )
    sunject = models.CharField(max_length =100  , verbose_name = "موضوع پیام")
    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"
        
        
    def __str__(self) :
        return self.name
    
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = "comments" ,verbose_name = "پست")
    name = models.CharField(max_length =50,verbose_name = "نام")
    body = models.TextField(verbose_name = "متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True,verbose_name = "تاریخ ساخت")
    updated = jmodels.jDateTimeField(auto_now=True ,verbose_name = "تاریخ ویرایش")
    active = models.BooleanField(default=False ,verbose_name = "وضعیت")
    class Meta:
        ordering = ['created']
        # for search index in table 
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"
        
        
    def __str__(self) :
        return f"{self.name} : {self.post}"
    
    