
from .models import CustomUser, UserProfile
from django.shortcuts import render
from evotingproject.settings import LOGIN_REDIRECT_URL, LOGIN_URL,LOGIN_URL_2
from .forms import UserProfileForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist


#Login decorator
@login_required(login_url=LOGIN_REDIRECT_URL)
#Handles user profile registration
def UserProf(request):
    user = request.user
    try:
      userprf = UserProfile.objects.get(user_id=user.id)
    except UserProfile.DoesNotExist:
      userprf = None
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            print("saved!!!!!!!!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            print("Invalid!!!!!")
            print(form.errors)
   
    context = {'form':form,'userprf':userprf}
    return render(request,"accounts/profilesetup.html", context)

def UserProf(request):
    user = request.user
    try:
      userprf = UserProfile.objects.get(user_id=user.id)
    except UserProfile.DoesNotExist:
      userprf = None
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            print("saved!!!!!!!!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            print("Invalid!!!!!")
            print(form.errors)
   
    context = {'form':form,'userprf':userprf}
    return render(request,"accounts/profilesetup.html", context)

@login_required(login_url=LOGIN_REDIRECT_URL)
#Handles updating of user profile
def UpdateUserProf(request):


    print("Fuck!!")
    # try:
    #   #ls2 = UserProfile.objects.all()
    #   ls2 = UserProfile.objects.get(user_id=user.id)
    # except UserProfile.DoesNotExist:
    #   ls2 = None

    form = UserProfileForm()
    try:
        userprf = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprf = UserProfile(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=userprf)
        if form.is_valid():
            form.save()
            
            return redirect(request.META['HTTP_REFERER'])
    else:
         form = UserProfileForm(instance=userprf)
         print(form.errors)
    context = {'form':form,'userprf':userprf}
    return render(request,"voter_profile.html", context)

#Handles updating of admin profile
@login_required(login_url=LOGIN_REDIRECT_URL)
@allowed_users(allowed_roles=['admin'])
def adminprf(request):
    userprf = CustomUser.objects.get(id=request.user.id)
    try:
       prof = request.user
    except CustomUser.DoesNotExist:
      prof = CustomUser(id=request.user.id)

    form = CustomUserChangeForm()
    print("Hey")

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES,instance=prof)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Successfully saved!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            print("Invalid!!!!!")
            print(form.errors)
   
    context = {'form':form,'userprf':userprf}
    return render(request,"admin/admin_profile.html", context)
    
def LoginUser(request):
    

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                user = request.user
                if request.user.groups.all()[0].name == 'admin':
                    return redirect("evoting:mainad")
            try:
                userprf = UserProfile.objects.get(user_id=user.id)
            except UserProfile.DoesNotExist:
                userprf = None

            if userprf:
                return redirect(LOGIN_URL)
            else:
                return redirect(LOGIN_URL_2)
        else:
            messages.error(request,'username or password not correct')
            return redirect(LOGIN_REDIRECT_URL)
        
                
    else:
        form = AuthenticationForm()
    return render(request,'signin.html',{'form':form})

  
@login_required(login_url=LOGIN_REDIRECT_URL)
def voterprf(request):
  
  try:
    userprf = UserProfile.objects.all()
  except UserProfile.DoesNotExist:
    userprf = None

  context = {'userprf':userprf}
  
  return render(request, 'accounts/voterprf.html',context)

@login_required(login_url=LOGIN_REDIRECT_URL)
@allowed_users(allowed_roles=['admin'])
def profilesetup(request):
  return render(request, 'accounts/profilesetup.html')

#Handles user changing of password
@login_required(login_url=LOGIN_REDIRECT_URL)
def changepad(request):
    if request.method == 'POST':
        old_password = request.POST.get("currentpass")
        new_password = request.POST.get("newpass")
        confirmed_new_password = request.POST.get("confirmpass")

        if old_password and new_password and confirmed_new_password:
            if request.user.is_authenticated:
                user = CustomUser.objects.get(email= request.user.email)
                if not user.check_password(old_password):
                    messages.warning(request, "your old password is not correct!")
                else:
                    if new_password != confirmed_new_password:
                        messages.warning(request, "your new password does not match!")
                    
                    elif len(new_password) < 8 or new_password.lower() == new_password or \
                         new_password.upper() == new_password or new_password.isalnum() or \
                         not any(i.isdigit() for i in new_password):
                        messages.warning(request, "your password is too weak!")

                    

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(request, "your password has been changed successfuly.!")

                        return redirect('accounts:adminprf')

        else:
            messages.warning(request, " sorry, all fields are required!")
 


    context = {

    }
    return render(request, "accounts/change_password_ad.html", context)

#handles change password for admin
@login_required(login_url=LOGIN_REDIRECT_URL)
@allowed_users(allowed_roles=['admin'])
def changepadvtr(request):

    if request.method == 'POST':
        old_password = request.POST.get("currentpass")
        new_password = request.POST.get("newpass")
        confirmed_new_password = request.POST.get("confirmpass")

        if old_password and new_password and confirmed_new_password:
            if request.user.is_authenticated:
                user = CustomUser.objects.get(email= request.user.email)
                if not user.check_password(old_password):
                    messages.warning(request, "your old password is not correct!")
                else:
                    if new_password != confirmed_new_password:
                        messages.warning(request, "your new password does not match!")
                    
                    elif len(new_password) < 8 or new_password.lower() == new_password or \
                         new_password.upper() == new_password or new_password.isalnum() or \
                         not any(i.isdigit() for i in new_password):
                        messages.warning(request, "your password is too weak!")

                    

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(request, "your password has been changed successfuly.!")

                        return redirect('accounts:regvoterprf')

        else:
            messages.warning(request, " sorry, all fields are required!")
 


    context = {

    }
    return render(request, "change_password_voter.html", context)

