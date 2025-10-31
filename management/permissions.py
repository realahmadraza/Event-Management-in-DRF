from rest_framework.permissions import BasePermission


class IsOrganizerOrReadOnly(BasePermission):
    message = 'Only the organizer can edit or delete this event.'
    def has_object_permission(self, request, view, obj):
        # read permissions allowed to any
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.organizer == request.user

class IsInvitedOrPublic(BasePermission):
    message = 'You are not invited to this private event.'
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        # allow organizer
        if obj.organizer == request.user:
            return True
        # invited users
        return request.user in obj.invited.all()