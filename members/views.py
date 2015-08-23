# members.views
# Views for the members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:25:37 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the members app.
"""

##########################################################################
## Imports
##########################################################################

from braces.views import LoginRequiredMixin
from members.permissions import IsAdminOrSelf
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from members.serializers import UserSerializer, PasswordSerializer

##########################################################################
## Views
##########################################################################


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A simple template view to display a member's profile.
    """

    template_name = "site/profile.html"

    def get_context_data(self, **kwargs):
        """
        Adds contextual information to the profile view.
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context

##########################################################################
## API HTTP/JSON Views
##########################################################################


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'], permission_classes=[IsAdminOrSelf])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
