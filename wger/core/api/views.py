# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status

from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit)
from wger.core.api.serializers import (
    UsernameSerializer,
    LanguageSerializer,
    DaysOfWeekSerializer,
    LicenseSerializer,
    RepetitionUnitSerializer,
    WeightUnitSerializer,
    UserprofileSerializer,
    UserCreateSerializer
)

from wger.utils.permissions import UpdateOnlyPermission, WgerPermission
from wger.config.models import GymConfig
from wger.gym.models import GymUserConfig


class UserCreateViewset(viewsets.ModelViewSet):
    '''
    API endpoint to create new users
    '''
    # protected endpoint
    is_private = True

    def create(self, request):
        request_data = JSONParser().parse(request)

        # get user profile
        user_profile = UserProfile.objects.get(user=request.user)
        
        # check if user is allowed to create users via API

        if user_profile.can_create_user:
            password = request_data.get('password', None)
            confirm_password = request_data.get('password', None)
            email = request_data.get('email', None)
            username = request_data.get('username', None)

            # ensure a username exists
            if not username:
                return Response({'message': 'A username is required!'}, status=status.HTTP_400_BAD_REQUEST)

            # check passwords match don't match return 400
            if password and confirm_password and password != confirm_password:
                return Response({'message': 'Passwords provided do not match!'}, status=status.HTTP_400_BAD_REQUEST)
            
            # pass request data through serializer
            user_serializer = UserCreateSerializer(data=request_data)
            
            # check if serializer is valid
            if user_serializer.is_valid():
                # get creator ID by introspecting token
                creator = User.objects.get(pk=Token.objects.get(key=request.auth).user_id)
                data = user_serializer.data
                username, email, password = data.get('username'), data.get('email', None), data.get('password')

                # create a user object
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # create user profile
                user.userprofile.creator = creator.username
                user.userprofile.token = request.auth.key
                
                # assign user a gym
                gym_config = GymConfig.objects.get(pk=1)
                if gym_config.default_gym:
                    user.userprofile.gym = gym_config.default_gym

                    # Create gym user configuration object
                    config = GymUserConfig()
                    config.gym = gym_config.default_gym
                    config.user = user
                    config.save()
                
                user.userprofile.save()
                return Response({"message": "You have successfully created user: {}".format(username)}, status=status.HTTP_201_CREATED)
            
            # if serializer is invalid
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # if user is not allowed to create users via API
        return Response({"message": "You are not authorised to create users via API"}, status=status.HTTP_403_FORBIDDEN)


class UserProfileViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for workout objects
    '''
    is_private = True
    serializer_class = UserprofileSerializer
    permission_classes = (WgerPermission, UpdateOnlyPermission)
    ordering_fields = '__all__'

    def get_queryset(self):
        '''
        Only allow access to appropriate objects
        '''
        return UserProfile.objects.filter(user=self.request.user)

    def get_owner_objects(self):
        '''
        Return objects to check for ownership permission
        '''
        return [(User, 'user')]

    @detail_route()
    def username(self, request, pk):
        '''
        Return the username
        '''

        user = self.get_object().user
        return Response(UsernameSerializer(user).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name')


class DaysOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = DaysOfWeek.objects.all()
    serializer_class = DaysOfWeekSerializer
    ordering_fields = '__all__'
    filter_fields = ('day_of_week', )


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name',
                     'url')


class RepetitionUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for repetition units objects
    '''
    queryset = RepetitionUnit.objects.all()
    serializer_class = RepetitionUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class WeightUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for weight units objects
    '''
    queryset = WeightUnit.objects.all()
    serializer_class = WeightUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )
