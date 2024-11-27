from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
import re
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
            # Robust Excel reading
            df = pd.read_excel(document.document.path, engine='openpyxl')
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Convert columns to numeric where possible
            numeric_columns = df.select_dtypes(exclude=['object']).columns
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {str(e)}")
            return redirect('student_performance')

        # Comprehensive list of possible SGPA columns
        all_semester_columns = [
            'SGPA-I', 'SGPA-II', 'SGPA-III', 'SGPA-IV', 
            'SGPA-V', 'SGPA-VI', 'SGPA-VII', 'SGPA-VIII',
            'SGPA I', 'SGPA II', 'SGPA III', 'SGPA IV',
            'SGPA V', 'SGPA VI', 'SGPA VII', 'SGPA VIII',
            'SGPA-1', 'SGPA-2', 'SGPA-3', 'SGPA-4',
            'SGPA 1', 'SGPA 2', 'SGPA 3', 'SGPA 4'
        ]
        
        # Find which semester columns actually exist in the dataframe
        existing_sgpa_columns = [col for col in all_semester_columns if col in df.columns]

        # Verbose logging of column detection
        print("All columns:", df.columns.tolist())
        print("Detected SGPA columns:", existing_sgpa_columns)

        # Check for required core columns
        required_columns = ['SL.NO', 'USN', 'NAME', 'CGPA', 'DETAINED?']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            messages.error(request, f"Missing core columns: {', '.join(missing_columns)}")
            return redirect('student_performance')
        
        if not existing_sgpa_columns:
            messages.error(request, "No semester SGPA columns found!")
            return redirect('student_performance')

        # Semester metrics calculation with more flexible extraction
        semester_metrics = {}
        for col in existing_sgpa_columns:
            # Extract semester identifier flexibly
            try:
                sem = col.split()[-1] if 'SGPA' in col else col.split('-')[-1]
            except:
                sem = 'Unknown'
            
            # Calculate semester-specific metrics
            semester_metrics[sem] = {
                'avg_sgpa': df[col].mean(),
                'max_sgpa': df[col].max(),
                'min_sgpa': df[col].min(),
                'successful_students': len(df[(df[col] >= 4.0) & (df['DETAINED?'] != 'YES')])
            }

        # Normalize detention status
        df['DETAINED?'] = df['DETAINED?'].fillna('NO').str.upper()

        # Calculate total number of students and other metrics
        total_students = len(df)
        successful_students = df[df['DETAINED?'] != 'YES']
        total_successful_students = len(successful_students)
        
        # CGPA calculations
        total_cgpa = df['CGPA'].sum()
        class_avg_cgpa = total_cgpa / total_students if total_students > 0 else 0
        detained_count = len(df[df['DETAINED?'] == 'YES'])

        # Create matplotlib figure
        plt.figure(figsize=(20, 12))
        plt.suptitle(f'Comprehensive Performance Analysis - {performance.academic_year}', fontsize=16)

        # Color palette
        color_palette = [
            '#3498db', '#2ecc71', '#e74c3c', '#f39c12', 
            '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
        ]

        # Subplot 1: Semester-wise SGPA Performance
        plt.subplot(2, 2, 1)
        semester_avgs = [semester_metrics[sem]['avg_sgpa'] for sem in semester_metrics]
        semester_labels = list(semester_metrics.keys())
        
        plt.bar(semester_labels, semester_avgs, color=color_palette[:len(semester_labels)], edgecolor='black')
        plt.title('Semester-wise Average SGPA', fontweight='bold')
        plt.xlabel('Semester')
        plt.ylabel('Average SGPA')
        plt.ylim(0, 10)
        
        # Add value labels
        for i, v in enumerate(semester_avgs):
            plt.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        # Subplot 2: Detention Status
        plt.subplot(2, 2, 2)
        plt.pie(
            [detained_count, total_students - detained_count], 
            labels=['Detained', 'Not Detained'], 
            autopct='%1.1f%%',
            colors=['#e74c3c', '#2ecc71']
        )
        plt.title('Detention Status', fontweight='bold')

        # Subplot 3: Performance Summary
        plt.subplot(2, 2, 3)
        plt.axis('off')

        # Generate summary text
        summary_lines = [
            f"Total Students: {total_students}",
            f"Successful Students: {total_successful_students}",
            f"Average CGPA: {class_avg_cgpa:.2f}",
            f"Detained Students: {detained_count}\n"
        ]

        # Add semester performance details
        summary_lines.append("Semester Performance:")
        for sem, metrics in semester_metrics.items():
            summary_lines.append(
                f"Sem {sem}: Avg SGPA {metrics['avg_sgpa']:.2f}, "
                f"Max SGPA {metrics['max_sgpa']:.2f}, "
                f"Successful Students {metrics['successful_students']}"
            )

        # Join the summary lines
        summary_text = "\n".join(summary_lines)

        plt.text(0.5, 0.5, summary_text, 
                 horizontalalignment='center', 
                 verticalalignment='center', 
                 fontsize=10, 
                 fontweight='bold',
                 bbox=dict(facecolor='white', alpha=0.7))
        plt.title('Performance Insights', fontweight='bold')

        # Subplot 4: Successful Students per Semester
        plt.subplot(2, 2, 4)
        successful_per_sem = [semester_metrics[sem]['successful_students'] for sem in semester_metrics]
        
        plt.bar(semester_labels, successful_per_sem, 
                color=color_palette[2:len(semester_labels)+2], 
                edgecolor='black')
        plt.title('Successful Students per Semester', fontweight='bold')
        plt.xlabel('Semester')
        plt.ylabel('Number of Successful Students')
        
        # Add value labels
        for i, v in enumerate(successful_per_sem):
            plt.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')

        # Save the plot
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        chart_image = base64.b64encode(buffer.getvalue()).decode('utf8')
        plt.close() 

        # Prepare chart data for saving
        chart_data = {
            'performance': performance,
            'chart_image': chart_image,
            'avg_cgpa': class_avg_cgpa,
            'total_students': total_students,
            'detained_count': detained_count,
            'total_cgpa': total_cgpa,
            'semester_averages': {sem: metrics['avg_sgpa'] for sem, metrics in semester_metrics.items()}
        }

        # Update or create PerformanceChart
        performance_chart, created = PerformanceChart.objects.update_or_create(
            performance=performance,
            defaults=chart_data
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