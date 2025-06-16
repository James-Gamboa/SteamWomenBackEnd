# permissions.py
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class IsRol(BasePermission):
    """
    Permiso personalizado que verifica si el usuario tiene un rol específico
    basado en el payload del token JWT.
    """
    
    # def has_permission(self, request, view):
        
    #     # 1. Autenticación JWT
    #     try:
    #         auth = JWTAuthentication().authenticate(request)
    #         if auth is None:
    #             self.message = "Token de autenticación no proporcionado"
    #             return False
                
    #         user, token = auth  # Desestructuramos la tupla de autenticación
            
    #     except AuthenticationFailed as e:
    #         self.message = f"Error de autenticación: {str(e)}"
    #         return False

    #     # 2. Obtener rol del payload del token
    #     role = token.payload.get('role')
    #     if not role:
    #         self.message = "El token no contiene información de rol"
    #         return False

    #     # 3. Obtener roles requeridos de la vista
    #     required_roles = getattr(view, 'required_roles', [])
    #     if not required_roles:
    #         self.message = "La vista no especificó roles requeridos"
    #         return False

    #     # 4. Verificar coincidencia de roles
    #     if role not in required_roles:
    #         self.message = f"Acceso denegado. Roles permitidos: {', '.join(required_roles)}"
    #         return False

    #     return True
    
    def has_permission(self, request, view):
        # 1. Autenticación JWT
        try:
            auth = JWTAuthentication().authenticate(request)
            if auth is None:
                self.message = "Token de autenticación no proporcionado"
                return False
                
            user, token = auth  # Desestructuramos la tupla de autenticación
            
        except AuthenticationFailed as e:
            self.message = f"Error de autenticación: {str(e)}"
            return False

        # 2. Obtener rol del payload del token
        role = token.payload.get('role')
        if not role:
            self.message = "El token no contiene información de rol"
            return False

        # 3. Obtener roles requeridos de la vista
        required_roles = getattr(view, 'required_roles', [])
        if not required_roles:
            self.message = "La vista no especificó roles requeridos"
            return False

        # 4. Verificar coincidencia de roles
        if role not in required_roles:
            self.message = f"Acceso denegado. Roles permitidos: {', '.join(required_roles)}"
            return False

        return True