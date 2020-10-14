from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('email', 'password1', 'password2')
        help_texts = {
            'email': None,
            'password1': None,
            'password2': None,

        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('email',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ('email', 'password')


class ShippingAddressForm(forms.Form):

    address = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                            'type': "text",
                                                            'placeholder': "Address.."
                                                            }))

    city = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                         'type': "text",
                                                         'placeholder': "city.."
                                                         }))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                          'type': "text",
                                                          'placeholder': "state.."
                                                          }))

    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                            'type': "text",
                                                            'placeholder': "zipcode.."
                                                            }))
