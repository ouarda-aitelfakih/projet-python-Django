from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, 'Accès refusé. Réservé aux administrateurs.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_teacher or request.user.is_admin):
            messages.error(request, 'Accès refusé. Réservé aux enseignants.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_student or request.user.is_admin):
            messages.error(request, 'Accès refusé. Réservé aux étudiants.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_roles = []
            if request.user.is_admin:
                user_roles.append('admin')
            if request.user.is_teacher:
                user_roles.append('teacher')
            if request.user.is_student:
                user_roles.append('student')
            
            if not any(role in user_roles for role in roles):
                role_names = {
                    'admin': 'administrateur',
                    'teacher': 'enseignant', 
                    'student': 'étudiant'
                }
                required_roles = [role_names.get(r, r) for r in roles]
                messages.error(request, f'Accès refusé. Rôle(s) requis : {", ".join(required_roles)}.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
