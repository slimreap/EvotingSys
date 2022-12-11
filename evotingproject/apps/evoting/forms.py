from django.forms import ModelForm
from django.forms import forms
# from django.contrib.auth.forms import AuthenticationForm
from .models import PartyList
from django import forms

#form for adding partylist name
class PartylistForm(ModelForm):
    class Meta:
        model = PartyList
        fields = ['partylist_name',]

#form for adding candidates profile

class PlatformForm(forms.Form):
    platform = forms.CharField(max_length=200,required=False)
    platform2 = forms.CharField(max_length=200,required=False)
    platform3 = forms.CharField(max_length=200,required=False)
   

class VoteTrackerForm(forms.Form):
    mayor = forms.CharField(max_length=200, required=True)
    vmayor = forms.CharField(max_length=200, required=True)
    senator = forms.CharField(max_length=200, required=True)
    councilor = forms.CharField(max_length=200, required=False)
   


class CandidateProfileForm(forms.Form):
    Candidate_Img = forms.ImageField(required=False)
    name = forms.CharField(max_length=200,required=False)


class UpdatePartylist(forms.Form):
    Candidate_Img = forms.ImageField(required=False)
    name = forms.CharField(max_length=200,required=False)
    platform = forms.CharField(max_length=200,required=False)
    platform2 = forms.CharField(max_length=200,required=False)
    platform3 = forms.CharField(max_length=200,required=False)
    partylist_name = forms.CharField(max_length=200,required=False)


#form for adding position and assign partylist to the candidates

