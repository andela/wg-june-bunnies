# -*- coding: utf-8 *-*

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

import sys

from django.utils.timezone import now
from django.core.management.base import BaseCommand
from wger.core.models import User


class Command(BaseCommand):
    '''
    Helper admin command to give user permission to create users over REST API
    '''

    help = 'Give permission to create users over REST API'

    def add_arguments(self, parser):
        '''
        Should receive positional argument: (username)
        '''
        parser.add_argument('username', nargs='?', type=str)
    
    def handle(self, **kwargs):
        '''Get user and change his/her permission to create users via REST API'''

        username = kwargs.get('username', None)
        # check if username has been provided
        if username:
            
            try:
                user = User.objects.get(username=username)
                # check if user already has permission to create users if not grant permission
                if user.userprofile.can_create_user:
                    print("\nUser: \'{}\' already has permission to create users over REST API".format(username))
                else:
                    user.userprofile.can_create_user = True
                    user.userprofile.save()
                    print("\nUser: \'{}\' has been granted permission to create users over REST API".format(username))
            except:
                # if user was not available
                print("\nUsername: \'{}\' does not exist. Confirm that it was typed correctly".format(username))
        else:
            print("\nYou have to provide a username for the user you wish to grant permission.")