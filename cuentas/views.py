from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def perfil(request):
    return render(request, 'cuentas/perfil.html', {'usuario': request.user})

def custom_logout(request):
    logout(request)
    return redirect('cuentas:login')
