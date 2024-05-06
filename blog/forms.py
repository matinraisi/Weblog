from django import forms
from .models import Comment , Post
from django.contrib.auth.models import User

class TicketForm(forms.Form):
     subject_select = (
         ("پیشنهاد" , "پیشنهاد"),
         ("انتقاد" , "انتقاد"),
         ("گزارش" , "گزارش")
     )
     name = forms.CharField(max_length =50 , required=True)
     massege = forms.CharField(widget = forms.Textarea , required=True)
     email = forms.EmailField()
     phone = forms.CharField(max_length =11   , required=True)
     sunject = forms.ChoiceField(choices=subject_select)
    
    
     def clean_phone(self):
         data = self.cleaned_data["phone"]
         if data:
              if not data.isnumeric:
                   raise forms.ValidationError("شماره تلفن اشتباه وارد شده است باید عدد باشد !")
              else:
                   return data
class CommentForm(forms.ModelForm):      
     def clean_name(self):
         name = self.cleaned_data["name"]
         if name :
              if len(name)<3:
                   raise forms.ValidationError("نام کوتاه است!")
              else:
                   return name
     class Meta:
          model = Comment
          # exclude = ['created']
          fields = ['name','body']
class PostForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all() ,required=True)
    title = forms.CharField(max_length =50 , required=True)
    description = forms.CharField(widget = forms.Textarea , required=True)
    slug = forms.SlugField(max_length =50 , required=True)
    status_choices = (
        ('DF', 'Draft'),
        ('PB', 'Publish'),
        ('RJ', 'Rejected')
     )
    status = forms.ChoiceField(choices = status_choices ,required=True)    
    reading_time = forms.IntegerField(required=True)

    def clean_title(self):
         title = self.cleaned_data["title"]
         if title:
              if len(title)<3:
                   raise forms.ValidationError("نام کوتاه است!")
              else:
                    return title
               
class CratePost(forms.ModelForm):
     image1 = forms.ImageField(label='تصویر اول')
     image2 = forms.ImageField(label='تصویر دوم')
     class Meta:
          model = Post
          fields = ['title','description','reading_time',]
class SearchForm(forms.Form):
     query = forms.CharField()