from email.policy import default
from random import choices
from tabnanny import verbose
from django.forms import ModelForm
from django import forms
from .models import category, musictrack, music_reviews

class QuestionForm1(forms.Form):
    ANSWERS_CHOICES1 =[ ("Happy","Happy"),("Sad","Sad") ,("Angry","Angry") , ("Stressed","Stressed"),]
    ANSWERS_CHOICES2 =[ ("Studious","Studious"),("Sleepy","Sleepy") ,("Relaxing","Relaxing") , ("Travelling","Travelling"),]
    # ANSWERS_CHOICES2 = {"Studious":"Studious", "Sleepy":"Sleepy", "Relaxing":"Relaxing", "Travelling":"Travelling"}
  
    question1 = "How are you feelin now?"
    question2 = "What are you doing now?"

    question1 = forms.ChoiceField(label="How are you feelin now?",choices = ANSWERS_CHOICES1,widget=forms.RadioSelect)
    question2 = forms.ChoiceField(label="What are you doing now?",choices = ANSWERS_CHOICES2,widget=forms.RadioSelect)

    question1 = forms.ModelChoiceField(queryset = category.objects.all() , initial=0, widget=forms.RadioSelect)

    question1.widget.attrs.update({'class':'answer'})
    question2.widget.attrs.update({'class':'answer'})

class QuestionForm(forms.Form):
    question1 = forms.ModelChoiceField(queryset = category.objects.all() , initial=0, widget=forms.RadioSelect)

    question1.widget.attrs.update({'class':'answer'})

class SearchForm(forms.Form):
    searchkey = forms.CharField(max_length=50,)
    searchkey.widget.attrs.update({'class':'form-control form-control-lg','placeholder':'Search your music here'})


class ReviewForm(forms.Form):
    reviewtext = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"rows":5, "cols":30, "placeholder":".... type your review here"}))

    
class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = music_reviews
        fields = ['review_text']


