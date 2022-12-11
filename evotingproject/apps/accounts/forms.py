import email
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import UserProfile
from .models import UserProfile as pq
from django.forms import forms
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



#Form for registering user
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','course','password1','password2']

#form for creating user profile
class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['User_Img','name','stud_id','course_year_and_section']

#form for creating admin profile
class AdminProfileForm(ModelForm):
  
    class Meta:
        model = CustomUser
        fields = ['User_Img','first_name']

#IGNORE THIS SHIT COZ I DON'T KNOW WHAT THIS IS
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

#form for updating admin profile
class CustomUserChangeForm(UserChangeForm):
    password = None
    email = None
    
    class Meta:
        model = CustomUser
        fields = ('User_Img','first_name')
