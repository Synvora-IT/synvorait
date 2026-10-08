from .models import Message , Blog , Project
from django import forms 

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["name" , "email" , "country" , "phone" , "subject" , "body" , "service" , "gender"]


    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        for field_name , field in self.fields.items():
            field.widget.attrs.update({"id":field_name , "placeholder":field_name.capitalize()})
            field.label_suffix = ""

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title" , "short_description" , "description" , "tags" , "banner"]

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        exclude = ["user"]

        widgets = {
            "start_date":forms.DateInput(
                attrs = {
                    "type":"date",
                }
            ),

            "end_date":forms.DateInput(
                attrs = {
                    "type":"date",
                    'format': '%Y-%m-%d'
                }
            )
        }