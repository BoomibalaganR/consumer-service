# from rest_framework.permissions import BasePermission


# class IsConsumerAuthenticated(BasePermission):
#     """
#     Allows access only to authenticated consumers.
#     """

#     def has_permission(self, request, view):
#         user = getattr(request, 'user', None)
        
#         return user is not None and isinstance(user, Consumer) and user.is_authenticated
