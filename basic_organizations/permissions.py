from rest_framework import permissions


class IsCoworker(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.user.is_staff or obj==request.user):
            return True
        if(view.action == 'retrieve'):
            orgas = set(obj.myorganizations.values_list('id', flat=True)).union(
                set(obj.organizations.values_list('id', flat=True)))
            orgasauth = set(request.user.myorganizations.values_list('id', flat=True)).union(
                set(request.user.organizations.values_list('id', flat=True)))

            res = set(orgas).intersection(set(orgasauth))
            return len(res) != 0
        else:
            return False
