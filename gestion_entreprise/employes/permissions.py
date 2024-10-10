from rest_framework import permissions

class IsDirigeant(permissions.BasePermission):
    """
    Permission qui permet uniquement aux dirigeants d'accéder aux vues restreintes.
    """
    def has_permission(self, request, view):
        has_perm = request.user and request.user.is_authenticated and request.user.groups.filter(name='Dirigeant').exists()
        if not has_perm:
            request.message = 'Vous devez être un dirigeant pour accéder à cette ressource.'
        return has_perm
