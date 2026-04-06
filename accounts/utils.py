# accounts/utils.py
from django.shortcuts import redirect


def redirect_by_role(user):
    if user.role == 'admin':
        return redirect('accounts:admin_dashboard')

    if user.role == 'officer':
        if user.is_approved:
            return redirect('officers:officer_dashboard')
        else:
            return redirect('accounts:pending_approval')

    if user.role == 'farmer':
        return redirect('farmers:farmer_dashboard')
    
    if user.role == 'customer':
        return redirect('accounts:customer_dashboard')

    return redirect('accounts:login')
