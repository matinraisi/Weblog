from typing import Any
from django import forms


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





     
        
    