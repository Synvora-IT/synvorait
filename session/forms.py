from .models import CustomUser
from django import forms 


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {"type":"password"}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {"type":"password"}))
    class Meta:
        model = CustomUser
        exclude = ["user_type" , "is_active" , "is_superuser" , "is_staff" , "groups" , "user_permissions" , "date_joined" , "last_login"]

    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.order_fields(["first_name" , "last_name" , "username" , "email" , "image"])
        for field_name , field in self.fields.items():
            field.widget.attrs.update({"placeholder":field_name.replace("_" , " ").title()})
            field.label_suffix = " "

    def clean(self):
        cleaned_data =  super().clean()

        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            return self.add_error("confirm_password" , "Password didn't matched")


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "image"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "type":"password",
                "id":"password",
                "name":"password",
                "placeholder":"Enter Old Password",
            }
        ),
        label_suffix = " "
    )

    new_password = forms.CharField(
            widget = forms.PasswordInput(
                attrs = {
                    "type":"password",
                    "id":"new_password",
                    "name":"new_password",
                    "placeholder":"Enter New Password"
                }
            ),
            label_suffix = " "
        )

    confirm_password = forms.CharField(
                widget = forms.PasswordInput(
                    attrs = {
                        "type":"password",
                        "id":"confirm_password",
                        "name":"confirm_password",
                        "placeholder":"Confirm Password"
                    }
                ),
                label_suffix = " "
            )