from tkinter import Widget
from django import forms
from .models import User

class UserLoginform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password']
		widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }

class UserSignupform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password','username']
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control item', 'placeholder':'닉네임'}),
            'email': forms.EmailInput(attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }

class Smsform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['phone_number']

		widgets = {
			'phone_number' : forms.TextInput(attrs={'class':'profile_smsInput', 'placeholder':'휴대폰 번호를 입력하세요.'}),

		}

class Smscheckform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['auth_number']
		widgets = {
			'auth_number' : forms.TextInput(attrs={'class':'profile_smsInput', 'placeholder':'인증번호를 입력하세요.'}),

		}