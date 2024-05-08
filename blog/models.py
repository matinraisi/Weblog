from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from datetime import datetime
from django.template.defaultfilters import slugify
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
    reading_time = models.PositiveIntegerField(verbose_name = "تایم مطالعه")
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

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def delete(self , *args , **kwargs):
        for img in self.images.all():
            storage , path = img.Image_file.storage , img.Image_file.path
            storage.delete(path)
        super().delete(*args,**kwargs)


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
    
    
def upload_to(instance, filename):
    # دریافت تاریخ و زمان فعلی
    now = datetime.now()
    # تعیین مسیر آپلود بر اساس سال
    upload_path = os.path.join('Post_image', str(now.year))
    # تعیین نام فایل
    _, ext = os.path.splitext(filename)
    file_name = f'{instance.pk}{ext}'
    # ترکیب مسیر آپلود و نام فایل
    return os.path.join(upload_path, file_name)
class ImagePost(models.Model):
     post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = "images" ,verbose_name = "پست")
     Image_file = ResizedImageField(upload_to=upload_to , crop=['middle', 'center'] , size=[500,500],quality=75)
     title = models.CharField(max_length =50 , null=True,blank=True , verbose_name = "عنوان")
     description = models.CharField(max_length =255,null=True,blank=True , verbose_name = "توضیحات")
     created = jmodels.jDateTimeField(auto_now_add=True)
     
     class Meta:
        ordering = ['created']
        # for search index in table 
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر پست"
        verbose_name_plural = "تصویر پست ها"       
     def __str__(self) :
        return self.title if self.title else self.Image_file.name
    
    
@receiver(pre_delete, sender=ImagePost)
def delete_image_file(sender, instance, **kwargs):
    # بدست آوردن مسیر فایل
    image_path = instance.Image_file.path
    
    # حذف فایل
    if os.path.isfile(image_path):
        os.remove(image_path)