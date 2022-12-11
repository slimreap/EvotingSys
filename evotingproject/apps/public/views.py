from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from evotingproject.apps.accounts.forms import RegistrationForm
from django.contrib.auth.models import Group
from evotingproject.apps.evoting.models import CandidateProfile, votes, votetracker
from django.contrib import messages


def Signup(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("valid!!!!")
            group = Group.objects.get(name='voter')
            user.groups.add(group)

            return redirect("public:home")
            
        else:
            print("invalid!!!!")
            messages.warning(request,str(form.errors))
            
    context = {'form':form}
    return render(request,"signup.html", context)

#jas view
def home(request):
    candidates = CandidateProfile.objects.all()
    vote = votes.objects.all()
    votetrack = votetracker.objects.all()
    context = {'candidates':candidates, 'vote':vote,'votetrack':votetrack}
    return render(request, 'home.html',context)
