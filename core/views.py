from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template.exceptions import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.db.models import Q

@ensure_csrf_cookie
def home(request):
    context = {
        'title': 'Welcome to Flow',
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'core/home.html', context)

@ensure_csrf_cookie
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                # Check if username or email already exists
                username = form.cleaned_data.get('username')
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is already taken.')
                    return render(request, 'registration/signup.html', {'form': form})
                
                user = form.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'title': 'Sign Up',
        'password_reset_available': True
    }
    return render(request, 'registration/signup.html', context)

@login_required
@ensure_csrf_cookie
def dashboard(request):
    try:
        # Get user-specific data
        user = request.user
        context = {
            'title': 'Dashboard',
            'user': user,
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            # Add more context data as needed for the dashboard
        }
        return render(request, 'core/dashboard.html', context)
    except TemplateDoesNotExist:
        messages.error(request, "Dashboard template not found.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred while loading the dashboard: {str(e)}")
        return redirect('home')

@login_required
@ensure_csrf_cookie
def settings(request):
    try:
        user = request.user
        context = {
            'title': 'Settings',
            'user': user,
            'email': user.email,
            'username': user.username,
            'date_joined': user.date_joined,
            'is_email_verified': hasattr(user, 'emailaddress') and user.emailaddress.verified,
            # Add more user settings as needed
        }
        return render(request, 'core/settings.html', context)
    except TemplateDoesNotExist:
        messages.error(request, "Settings template not found.")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"An error occurred while loading settings: {str(e)}")
        return redirect('dashboard')
