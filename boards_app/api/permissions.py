from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    """
    Custom object-level permission.

    Grants access if the requesting user is either:
    - the owner of the object, or
    - a member associated with the object.

    Intended for models that define:
    - an `owner` (or `owner_id`) field
    - a ManyToMany relation `members` to User
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user has permission to access the object.

        Conditions:
        - The user is the owner of the object, OR
        - The user is listed in the object's members relation

        Args:
            request: The current HTTP request.
            view: The DRF view handling the request.
            obj: The object being accessed.

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        user = request.user
        return (
            obj.owner_id == user.id
            or obj.members.filter(id=user.id).exists()
        )
