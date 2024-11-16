from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    SignupForm, 
    UserUpdateForm, 
    UserProfileUpdateForm, 
    CustomPasswordChangeForm,
    
)
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import UserProfile,AcademicYear,StudentDocument

def landing_page(request):
    """Handle the landing page with login functionality"""
    if request.user.is_authenticated:
        return redirect('homepage')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the next page if specified, otherwise go to homepage
                next_page = request.GET.get('next', 'homepage')
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'adminpage/landing_page.html', {'form': form})

def signup(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('homepage')
        
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Log the user in after successful registration
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome aboard!')
                return redirect('homepage')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            # Form is not valid, display specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignupForm()
    return render(request, 'adminpage/signup.html', {'form': form})

@login_required
def profile(request):
    """Handle user profile updates and password changes separately"""
    if request.method == 'POST':
        # Handle profile update
        if 'update_profile' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)

            if user_form.is_valid() and profile_form.is_valid():
                try:
                    user_form.save()
                    profile_form.save()
                    messages.success(request, 'Your profile has been updated successfully!')
                    return redirect('profile')
                except Exception as e:
                    messages.error(request, f'An error occurred while updating your profile: {str(e)}')
            else:
                for form in [user_form, profile_form]:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f'{field}: {error}')
        
        # Handle password change
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                try:
                    user = password_form.save(commit=False)
                    # Send confirmation email
                    send_mail(
                        'Password Change Confirmation',
                        'Your password has been successfully changed. If you did not make this change, please contact support immediately.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    user.save()
                    update_session_auth_hash(request, user)  # Keep user logged in
                    messages.success(request, 'Your password was changed successfully! A confirmation email has been sent.')
                    return redirect('profile')
                except Exception as e:
                    messages.error(request, f'An error occurred while changing your password: {str(e)}')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

    else:
        # Initial form load
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
        password_form = CustomPasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'adminpage/profile.html', context)
@login_required
def homepage(request):
    """Display the homepage for authenticated users"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create a new UserProfile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'adminpage/homepage.html', context)

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing_page')

@login_required
def delete_account(request):
    """Handle account deletion"""
    if request.method == 'POST':
        try:
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('landing_page')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting your account: {str(e)}')
            return redirect('profile')
    return render(request, 'adminpage/delete_account_confirmation.html')

@login_required
def change_email(request):
    """Handle email change with verification"""
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            try:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Your email has been updated successfully!')
            except Exception as e:
                messages.error(request, f'An error occurred while updating your email: {str(e)}')
        else:
            messages.error(request, 'Please provide a valid email address.')
        return redirect('profile')
    return redirect('profile')

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'adminpage/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, 'adminpage/500.html', status=500)
@login_required
def student_details_view(request):
    """Display and manage academic years and files."""
    batches = AcademicYear.objects.all()

    if request.method == 'POST':
        # Adding a new academic year
        if 'academic_year' in request.POST:
            academic_year = request.POST.get('academic_year')
            if academic_year:
                try:
                    AcademicYear.objects.create(academic_year=academic_year)
                    messages.success(request, f'Academic year "{academic_year}" added successfully.')
                except Exception as e:
                    messages.error(request, f'Error adding academic year: {str(e)}')
            else:
                messages.error(request, 'Please provide a valid academic year.')

        # Deleting an academic year
        if 'delete_batch' in request.POST:
            batch_id = request.POST.get('delete_batch')
            try:
                batch = AcademicYear.objects.get(id=batch_id)
                batch.delete()
                messages.success(request, f'Academic year "{batch.academic_year}" deleted successfully.')
            except AcademicYear.DoesNotExist:
                messages.error(request, 'The specified academic year does not exist.')
            except Exception as e:
                messages.error(request, f'Error deleting academic year: {str(e)}')

    return render(request, 'adminpage/student_details.html', {'batches': batches})


@login_required
def upload_file_view(request, batch_id):
    """Handle file upload for a specific academic year."""
    if request.method == 'POST':
        try:
            batch = AcademicYear.objects.get(id=batch_id)
            document = request.FILES['document']
            StudentDocument.objects.create(batch=batch, document=document)
            messages.success(request, 'File uploaded successfully.')
        except AcademicYear.DoesNotExist:
            messages.error(request, 'Academic year not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    return redirect('student_details')


