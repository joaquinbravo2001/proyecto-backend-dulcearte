from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def rol_requerido(roles_permitidos):
    """
    Decorador para restringir el acceso a vistas según el rol del usuario.
    Los administradores (is_superuser o rol 'admin') tienen acceso total.
    """
    if isinstance(roles_permitidos, str):
        roles_permitidos = [roles_permitidos]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('cuentas:login')
            
            # Superusuarios y administradores tienen acceso sin restricción
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            perfil = getattr(request.user, 'perfil', None)
            user_rol = perfil.rol if perfil else None

            if user_rol == 'admin' or user_rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            
            messages.error(
                request,
                f"Acceso denegado: tu rol actual ({user_rol or 'Sin rol'}) no tiene permisos para ingresar a este módulo."
            )
            return redirect('pedidos:dashboard')

        return _wrapped_view
    return decorator
