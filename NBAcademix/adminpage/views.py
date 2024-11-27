from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .models import StudentPerformance, Document ,  UserProfile, StudentList, StudentDocument, AchievementDocument, Achievement,PerformanceChart
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import base64
import io
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
from django.urls import reverse
from django.http import HttpResponseRedirect
import os
import zipfile
from io import BytesIO
from .forms import (
    SignupForm, 
    UserUpdateForm, 
    UserProfileUpdateForm, 
    CustomPasswordChangeForm,
    
)



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
def student_performance_view(request):
    """Display and manage student performance records."""
    performances = StudentPerformance.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Adding a new performance record
        if 'academic_year' in request.POST:
            academic_year_in = request.POST.get('academic_year_in')
            academic_year = request.POST.get('academic_year')
            
            if academic_year and academic_year_in:
                try:
                    performance = StudentPerformance.objects.create(
                        academic_year_in=academic_year_in,
                        academic_year=academic_year
                    )
                    messages.success(request, f'Performance record for {academic_year_in} Year ({academic_year}) added successfully.')
                except Exception as e:
                    messages.error(request, f'Error adding performance record: {str(e)}')
            else:
                messages.error(request, 'Please provide all required information.')
        return redirect('student_performance')
    
    # For GET requests, render the template with the performances data
    context = {
        'performances': performances,
    }
    return render(request, 'adminpage/student_performance.html', context)

@login_required
def delete_performance(request, performance_id):
    performance = get_object_or_404(StudentPerformance, id=performance_id)
    if request.method == 'POST':
        # This will also delete all related documents due to CASCADE
        performance.delete()
        messages.success(request, "Performance record deleted successfully")
        return redirect('student_performance')
    return redirect('student_performance')


@login_required
def upload_performance_file(request, performance_id):
    try:
        performance = get_object_or_404(StudentPerformance, id=performance_id)
        
        if request.method == 'POST' and request.FILES.get('document'):
            uploaded_file = request.FILES['document']
            
            # Create new Document instance
            document = Document(
                performance=performance,
                document=uploaded_file,
                original_filename=uploaded_file.name  # Store the original filename
            )
            document.save()
            
            messages.success(request, f'File "{uploaded_file.name}" uploaded successfully')
            return redirect('student_performance')
            
    except Exception as e:
        messages.error(request, f'Error uploading file: {str(e)}')
        
    return redirect('student_performance')

@login_required
def download_performance_files(request, performance_id):
    """Download all files for a specific performance record as a zip file."""
    try:
        performance = get_object_or_404(StudentPerformance, id=performance_id)
        documents = performance.documents.all()

        if not documents:
            messages.warning(request, 'No documents available to download.')
            return redirect('student_performance')

        # Create zip file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for document in documents:
                file_name = os.path.basename(document.document.name)
                zip_file.writestr(file_name, document.document.read())

        # Prepare response
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={performance.academic_year_in}_{performance.academic_year}_documents.zip'

        return response

    except Exception as e:
        messages.error(request, f'Error downloading files: {str(e)}')
        return redirect('student_performance')

@login_required
def delete_performance_file(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        performance = document.performance
        document.document.delete()  # Delete the actual file
        document.delete()  # Delete the database record
        messages.success(request, "File deleted successfully")
        return redirect('student_performance')
    return redirect('student_performance')

@login_required
def student_list_view(request):
    """Display and manage student lists."""
    student_lists = StudentList.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'batch_year' in request.POST:
            batch_year = request.POST.get('batch_year')
            
            if batch_year:
                try:
                    student_list = StudentList.objects.create(
                        batch_year=batch_year
                    )
                    messages.success(request, f'Student list for batch {batch_year} added successfully.')
                except Exception as e:
                    messages.error(request, f'Error adding student list: {str(e)}')
            else:
                messages.error(request, 'Please provide batch year.')
        return redirect('student_list')
    
    context = {
        'student_lists': student_lists,
    }
    return render(request, 'adminpage/student_list.html', context)

@login_required
def delete_student_list(request, list_id):
    student_list = get_object_or_404(StudentList, id=list_id)
    if request.method == 'POST':
        student_list.delete()
        messages.success(request, "Student list deleted successfully")
        return redirect('student_list')
    return redirect('student_list')

@login_required
def upload_student_file(request, list_id):
    try:
        student_list = get_object_or_404(StudentList, id=list_id)
        
        if request.method == 'POST' and request.FILES.get('document'):
            uploaded_file = request.FILES['document']
            
            document = StudentDocument(
                student_list=student_list,
                document=uploaded_file,
                original_filename=uploaded_file.name
            )
            document.save()
            
            messages.success(request, f'File "{uploaded_file.name}" uploaded successfully')
            return redirect('student_list')
            
    except Exception as e:
        messages.error(request, f'Error uploading file: {str(e)}')
        
    return redirect('student_list')

@login_required
def download_student_files(request, list_id):
    """Download all files for a specific student list as a zip file."""
    try:
        student_list = get_object_or_404(StudentList, id=list_id)
        documents = student_list.documents.all()

        if not documents:
            messages.warning(request, 'No documents available to download.')
            return redirect('student_list')

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for document in documents:
                file_name = os.path.basename(document.document.name)
                zip_file.writestr(file_name, document.document.read())

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={student_list.department}_{student_list.batch_year}_documents.zip'

        return response

    except Exception as e:
        messages.error(request, f'Error downloading files: {str(e)}')
        return redirect('student_list')

@login_required
def delete_student_file(request, document_id):
    document = get_object_or_404(StudentDocument, id=document_id)
    if request.method == 'POST':
        document.document.delete()
        document.delete()
        messages.success(request, "File deleted successfully")
        return redirect('student_list')
    return redirect('student_list')
@login_required
def achievement_view(request):
    """Display and manage achievements."""
    achievements = Achievement.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'event_name' in request.POST:
            event_name = request.POST.get('event_name')
            
            if event_name:
                try:
                    achievement = Achievement.objects.create(
                        event_name=event_name
                    )
                    messages.success(request, f'Achievement for event "{event_name}" added successfully.')
                except Exception as e:
                    messages.error(request, f'Error adding achievement: {str(e)}')
            else:
                messages.error(request, 'Please provide event name.')
        return redirect('achievement')
    
    context = {
        'achievements': achievements,
    }
    return render(request, 'adminpage/achievement.html', context)

@login_required
def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    if request.method == 'POST':
        achievement.delete()
        messages.success(request, "Achievement deleted successfully")
        return redirect('achievement')
    return redirect('achievement')

@login_required
def upload_achievement_file(request, achievement_id):
    try:
        achievement = get_object_or_404(Achievement, id=achievement_id)
        
        if request.method == 'POST' and request.FILES.get('document'):
            uploaded_file = request.FILES['document']
            
            document = AchievementDocument(
                achievement=achievement,
                document=uploaded_file,
                original_filename=uploaded_file.name
            )
            document.save()
            
            messages.success(request, f'File "{uploaded_file.name}" uploaded successfully')
            return redirect('achievement')
            
    except Exception as e:
        messages.error(request, f'Error uploading file: {str(e)}')
        
    return redirect('achievement')

@login_required
def download_achievement_files(request, achievement_id):
    try:
        achievement = get_object_or_404(Achievement, id=achievement_id)
        documents = achievement.documents.all()

        if not documents:
            messages.warning(request, 'No documents available to download.')
            return redirect('achievement')

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for document in documents:
                file_name = os.path.basename(document.document.name)
                zip_file.writestr(file_name, document.document.read())

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={achievement.event_name}_documents.zip'

        return response

    except Exception as e:
        messages.error(request, f'Error downloading files: {str(e)}')
        return redirect('achievement')

@login_required
def delete_achievement_file(request, document_id):
    document = get_object_or_404(AchievementDocument, id=document_id)
    if request.method == 'POST':
        document.document.delete()
        document.delete()
        messages.success(request, "File deleted successfully")
        return redirect('achievement')
    return redirect('achievement')

@login_required
def generate_performance_chart(request, document_id):
    try:
        # Get the performance document
        document = get_object_or_404(Document, id=document_id)
        performance = document.performance

        # Validate file extension
        file_extension = os.path.splitext(document.document.path)[1].lower()
        allowed_extensions = ['.xls', '.xlsx']
        
        if file_extension not in allowed_extensions:
            messages.error(request, "Invalid file type. Please upload an Excel file.")
            return redirect('student_performance')

        # Read the Excel file with error handling
        try:
            df = pd.read_excel(document.document.path, engine='openpyxl')
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {str(e)}")
            return redirect('student_performance')

        # Flexible column matching
        def find_column(possible_names):
            for name in possible_names:
                matching_cols = [col for col in df.columns if name.lower() in col.lower()]
                if matching_cols:
                    return matching_cols[0]
            return None

        # Find columns flexibly
        sl_no_col = find_column(['sl.no', 'slno', 'serial', 'serial no'])
        usn_col = find_column(['usn', 'usr', 'user'])
        name_col = find_column(['name', 'student name'])
        sgpa_iii_col = find_column(['sgpa-iii', 'sgpa iii', 'sgpa 3'])
        sgpa_iv_col = find_column(['sgpa-iv', 'sgpa iv', 'sgpa 4'])
        cgpa_col = find_column(['cgpa', 'cpi'])
        detained_col = find_column(['detained?', 'detained', 'detention'])

        # Validate columns
        required_columns = {
            'SL.NO': sl_no_col,
            'USN': usn_col,
            'NAME': name_col,
            'SGPA-III': sgpa_iii_col,
            'SGPA-IV': sgpa_iv_col,
            'CGPA': cgpa_col,
            'DETAINED?': detained_col
        }

        # Check if all required columns are found
        missing_columns = [key for key, value in required_columns.items() if value is None]
        if missing_columns:
            messages.error(request, f"Missing columns: {', '.join(missing_columns)}")
            return redirect('student_performance')

        # Rename columns to standard names
        df = df.rename(columns={
            sl_no_col: 'SL.NO',
            usn_col: 'USN',
            name_col: 'NAME',
            sgpa_iii_col: 'SGPA-III',
            sgpa_iv_col: 'SGPA-IV',
            cgpa_col: 'CGPA',
            detained_col: 'DETAINED?'
        })

        # Calculate total number of students
        total_students = len(df)

        # Calculate total and average CGPA
        total_cgpa = df['CGPA'].sum()
        class_avg_cgpa = total_cgpa / total_students

        # Calculate semester-specific averages
        avg_sgpa_iii = df['SGPA-III'].mean()
        avg_sgpa_iv = df['SGPA-IV'].mean()

        # Count detained students (case-insensitive)
        detained_count = len(df[df['DETAINED?'].str.upper() == 'YES'])

        # Create matplotlib figure
        plt.figure(figsize=(12, 6))
        plt.suptitle(f'Class Performance - {performance.academic_year}', fontsize=16)


        # Subplot 1: Bar Chart - SGPA and CGPA Comparison
        plt.subplot(1, 2, 1)
        plt.bar(['Avg SGPA-III', 'Avg SGPA-IV', 'Avg CGPA'], 
                [avg_sgpa_iii, avg_sgpa_iv, class_avg_cgpa], 
                color=['maroon', 'navy', 'green'])
        plt.title('Performance Metrics')
        plt.ylabel('Score')
        plt.ylim(0, 10)  # Assuming scores are out of 10
        
        # Add value labels on top of each bar
        for i, v in enumerate([avg_sgpa_iii, avg_sgpa_iv, class_avg_cgpa]):
            plt.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        # Subplot 2: Pie Chart - Detention Status
        plt.subplot(1, 2, 2)
        plt.pie(
            [detained_count, total_students - detained_count], 
            labels=['Detained', 'Not Detained'], 
            autopct='%1.1f%%',
            colors=['#FF6B6B', '#4ECDC4']
        )
        plt.title('Detention Status')

        # Save the plot
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        chart_image = base64.b64encode(buffer.getvalue()).decode('utf8')
        plt.close() 

        # Update or create PerformanceChart
        performance_chart, created = PerformanceChart.objects.update_or_create(
            performance=performance,
            defaults={
                'chart_image': chart_image,
                'avg_cgpa': class_avg_cgpa,
                'avg_sgpa_iii': avg_sgpa_iii,
                'avg_sgpa_iv': avg_sgpa_iv,
                'total_students': total_students,
                'total_cgpa': total_cgpa,
                'detained_count': detained_count
            }
        )

        messages.success(request, "Performance chart generated successfully!")
        return redirect('student_performance')

    except Exception as e:
        messages.error(request, f"Error generating chart: {str(e)}")
        return redirect('student_performance')
    
@login_required
def download_performance_chart(request, performance_id):
    performance = get_object_or_404(StudentPerformance, id=performance_id)
    
    if not hasattr(performance, 'performance_chart'):
        messages.error(request, "No chart available for this performance record.")
        return redirect('student_performance')

    chart = performance.performance_chart
    
    # Create response
    response = HttpResponse(base64.b64decode(chart.chart_image), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="performance_chart_{performance.academic_year}.png"'
    return response