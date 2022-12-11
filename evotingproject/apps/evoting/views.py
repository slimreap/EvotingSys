from django.forms import formset_factory
from .models import Position, CandidateProfile, PartyList, Platform, votes, votetracker
from django.shortcuts import render
from evotingproject.settings import LOGIN_REDIRECT_URL
from .forms import CandidateProfileForm, PartylistForm, PlatformForm, VoteTrackerForm, UpdatePartylist
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from evotingproject.apps.accounts.models import UserProfile, CustomUser
from evotingproject.apps.accounts.decorators import allowed_users, authenticated_user

from django.contrib.auth.decorators import user_passes_test

def is_user(user):

    return user.is_authenticated



#handles adding of candidates
@allowed_users(allowed_roles=['admin'])
def addcandidate(request):
    
    party = PartyList.objects.all()
    cand = CandidateProfile.objects.select_related('partylist').all()
    plat = Platform.objects.prefetch_related('platform').all()
    partylist_form = PartylistForm()
    PlatformSet = formset_factory( PlatformForm,extra=7)
    candidateFormSet = formset_factory(CandidateProfileForm,extra=7)
    form1 = PlatformSet(prefix='platform')
    form2 = candidateFormSet(prefix='candidate')

    # position = Position.objects.values_list('name')
    if request.method == 'POST':
        partylist_form = PartylistForm(request.POST)
        form1 = PlatformSet(request.POST, prefix='platform')
        form2 = candidateFormSet(request.POST,request.FILES,prefix='candidate')

        if form1.is_valid() and form2.is_valid() and partylist_form.is_valid():
         
            count = 0
            try:
                partylist = PartyList.objects.get(partylist_name=request.POST['partylist_name'])
            except ObjectDoesNotExist:
                partylist = partylist_form.save()
            
            for f1 in form1:
                try:
                    p1 = f1.cleaned_data['platform']
                    p2 = f1.cleaned_data['platform2']
                    p3 = f1.cleaned_data['platform3']
                    platform = Platform(candidate_platform=p1,candidate_platform2=p2,candidate_platform3=p3)
                    platform.save()
                except KeyError:
                    continue
      
                # if  f1.cleaned_data("platform",None):
                #     pass
                # else:
                #     p1 = f1.cleaned_data['platform']
                #     p2 = f1.cleaned_data['platform2']
                #     p3 = f1.cleaned_data['platform3']
                #     platform = Platform(candidate_platform=p1,candidate_platform2=p2,candidate_platform3=p3)
                #     platform.save()


                # if Platform.objects.filter(candidate_platform=p1).exists():
                #     pass
                # else:


                for f2 in form2:
                    
                    try:
                            
                            name = f2.cleaned_data['name']
                            img = f2.cleaned_data['Candidate_Img']
                            if name and img:
                               
                                   
                                if CandidateProfile.objects.filter(name=name).exists():
                                    pass

                                else:
                                    candidate = CandidateProfile(Candidate_Img=img,name=name)
                                    candidate.save()
                                        
                                    candidate.platform = platform
                                        
                                    candidate.partylist = partylist
                                    if count == 0:
                                        candidate.position = Position.objects.get(id=1)
                                    elif count == 1:
                                        candidate.position = Position.objects.get(id=2)
                                    elif count == 2:
                                        candidate.position = Position.objects.get(id=3)
                                    elif count == 3:
                                        candidate.position = Position.objects.get(id=4)
                                    elif count == 4:
                                        candidate.position = Position.objects.get(id=5)
                                    elif count == 5:
                                        candidate.position = Position.objects.get(id=6)
                                    elif count == 6:
                                        candidate.position = Position.objects.get(id=7)
                                    candidate.save()
                                    count+=1
                                    break
                        
                    except KeyError:
                            count+=1
                            pass
                
                               
            print("saved!!!!!!!!")
            return redirect(request.META['HTTP_REFERER'])
        else:

            print(form1.errors)
            print(form2.errors)
            print(form1.non_form_errors)
            print(form2.non_form_errors)
            print("Invalid!!!!!")
            
   
    context = {'form1':form1,'form2':form2,'party':party,'cand':cand,'plat':plat}
    return render(request,"admin/admin_dashboard.html", context)



#handles displaying of candidates in candidate profile template
def candprf(request):
    party = PartyList.objects.all()
    candidate = CandidateProfile.objects.all()
    plat = Platform.objects.all()

    

    context = {'party':party,'candidate':candidate,'plat':plat}
    return render(request, 'accounts/candidates_profile.html',context)


def castedvotes(request):
    user = request.user
    vote = votes.objects.filter(voter_id=user.id)
    myls = list(vote)
    for values in myls:
        print(values.candidate.position)
    
    partylist = PartyList.objects.all()
    
    
    context = {'partylist':partylist,'myls':myls}
    return render(request, 'casted_vote.html', context)

@allowed_users(allowed_roles=['admin'])
def dashboardad(request):
    candidates = CandidateProfile.objects.all()
    vote = votes.objects.all()
    votetrack = votetracker.objects.all()
    context = {'candidates':candidates,'vote':vote, 'votetrack':votetrack}
    return render(request, 'admin/dash_in_admin.html',context)

def dashboardvtr(request):
    candidates = CandidateProfile.objects.all()
    vote = votes.objects.all()
    votetrack = votetracker.objects.all()
    context = {'candidates':candidates, 'vote':vote, 'votetrack':votetrack}
    return render(request, 'dash_in_voter.html', context)

def castvote(request):
    candidates = CandidateProfile.objects.all()
    user = request.user
    loggedinuser = UserProfile.objects.get(user_id=user.id)
  
    
    form = VoteTrackerForm()
    if request.method == 'POST':
        form = VoteTrackerForm(request.POST)
        
        if form.is_valid():

            for key, value in form.cleaned_data.items():
                

                vcandidate = votes(candidate_id=value)
                vcandidate.voter_id = loggedinuser.user_id
                
                vcandidate.save()

                try:
                    votetrack = votetracker.objects.get(candidate_id=value)
                except ObjectDoesNotExist:
                    votetrack = votetracker(candidate_id=value)
                votetrack.vote_count += 1
                votetrack.save()
 
            user.voted = True
    
    context = {'candidates':candidates,'form':form,'loggedinuser':loggedinuser}
    return render(request, 'cast_vote.html',context)


@allowed_users(allowed_roles=['admin'])
def mainad(request):
  return render(request, 'admin/main_admin.html')

@authenticated_user
def mainvtr(request):
    print(request.session)
    return render(request, 'main_voter.html')


@allowed_users(allowed_roles=['admin'])
def updateparty(request,id):
    # cand = CandidateProfile.objects.select_related('partylist').all()
    party = PartyList.objects.get(id=id)
    cand = CandidateProfile.objects.filter(partylist_id=id).order_by('position_id')
    plat = Platform.objects.prefetch_related('platform').all()
    
    partylist_form = PartylistForm()
    PlatformSet = formset_factory( PlatformForm,extra=7)
    candidateFormSet = formset_factory(CandidateProfileForm,extra=7)
    
    form1 = PlatformSet(prefix='platform')
    form2 = candidateFormSet(prefix='candidate')
    
    if request.method == "POST":
        partylist_form = PartylistForm(request.POST)
        form1 = PlatformSet(request.POST, prefix='platform')
        form2 = candidateFormSet(request.POST,request.FILES,prefix='candidate')
        
        if form1.is_valid() and form2.is_valid() and partylist_form.is_valid():
                party.partylist_name = partylist_form.cleaned_data['partylist_name']
                print(party.partylist_name)
                for candidate in cand:
                    
                    if candidate.position_id == 1:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-0-name']:
                            candidate.name = request.POST['candidate-0-name']
                            
                            if request.FILES.get('candidate-0-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-0-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-0-platform']
                            platform.candidate_platform2 = request.POST['platform-0-platform2']
                            platform.candidate_platform3 = request.POST['platform-0-platform3']
                            platform.save()

                    elif candidate.position_id == 2:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-1-name']:
                            candidate.name = request.POST['candidate-1-name']
                            
                            if request.FILES.get('candidate-1-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-1-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-1-platform']
                            platform.candidate_platform2 = request.POST['platform-1-platform2']
                            platform.candidate_platform3 = request.POST['platform-1-platform3']
                            platform.save()

                    elif candidate.position_id == 3:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-2-name']:
                            candidate.name = request.POST['candidate-2-name']
                            if request.FILES.get('candidate-2-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-2-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-2-platform']
                            platform.candidate_platform2 = request.POST['platform-2-platform2']
                            platform.candidate_platform3 = request.POST['platform-2-platform3']
                            platform.save()
                    elif candidate.position_id == 4:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-3-name'] and request.FILES.get('candidate-3-Candidate_Img'):
                            candidate.name = request.POST['candidate-3-name']
                            
                            if request.FILES.get('candidate-3-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-3-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-3-platform']
                            platform.candidate_platform2 = request.POST['platform-3-platform2']
                            platform.candidate_platform3 = request.POST['platform-3-platform3']
                            platform.save()


                    elif candidate.position_id == 5:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-4-name']:
                            candidate.name = request.POST['candidate-4-name']
                            
                            if request.FILES.get('candidate-4-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-4-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-4-platform']
                            platform.candidate_platform2 = request.POST['platform-4-platform2']
                            platform.candidate_platform3 = request.POST['platform-4-platform3']
                            platform.save()
                    elif candidate.position_id == 6:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-5-name']:
                            candidate.name = request.POST['candidate-5-name']
                            
                            if request.FILES.get('candidate-5-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-5-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-5-platform']
                            platform.candidate_platform2 = request.POST['platform-5-platform2']
                            platform.candidate_platform3 = request.POST['platform-5-platform3']
                            platform.save()

                    elif candidate.position_id == 7:
                        candidate = CandidateProfile.objects.get(name=candidate)
                        if request.POST['candidate-6-name']:
                            candidate.name = request.POST['candidate-6-name']
                            
                            if request.FILES.get('candidate-6-Candidate_Img'):
                                candidate.Candidate_Img = request.FILES.get('candidate-6-Candidate_Img')
                            candidate.save()
                            platform = Platform.objects.get(id=candidate.platform_id)
                            platform.candidate_platform = request.POST['platform-6-platform']
                            platform.candidate_platform2 = request.POST['platform-6-platform2']
                            platform.candidate_platform3 = request.POST['platform-6-platform3']
                            platform.save()


                   
                return redirect('evoting:addcandidate')
        else:

            print(form1.errors)
            print(form2.errors)
            print(form1.non_form_errors)
            print(form2.non_form_errors)
            print("Invalid!!!!!")
            

  
            

       

    context = {'party':party,'plat':plat,'cand':cand,'form1':form1,'form2':form2}
    return render(request, 'admin/admin_dashboardpartylistupdate.html',context)

@allowed_users(allowed_roles=['admin'])
def deleteparty (request,id):
    party = PartyList.objects.get(id=id)
    
    if party:
        party.delete()
        return redirect('evoting:addcandidate')
    return render(request,'admin/admin_dashboard.html')