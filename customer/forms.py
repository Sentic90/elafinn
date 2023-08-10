
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class CustomerAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm your Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        # Cheacks that the password entries matches
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password did't match")
        return password2

    def save(self, commit=True):
        # save the provided password in hash format
        user = super(CustomerAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_customer = True
        if commit:
            user.save()
        return user