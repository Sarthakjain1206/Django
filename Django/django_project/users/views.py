from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    print("I am called==================..")
    if request.method == "POST":
        print("I am inside post method call")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # To save the user's data in database, we need to apply this method only. 
            form.save()
            # For acknowledgement we are showing the success message to the user that account has been created.
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. Now, you can login to our website.')
            # After clicking on submit btn we do not want to show regiteration form back to user... so we are redirecting the user to home page.
            return redirect('login')
    else:
        print("I am inside get  ethod call")
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

# This decorator provides the functionality of redirecting to login page if user tries to access the profile page and user is not logged in.
# Also we have to add one line in settings.py file to make it work (we have to include url name of login page)  
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
