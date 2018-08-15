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


from django.core.management.base import BaseCommand
from wger.core.models import User
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    Helper admin command to list users created over REST API by a creator
    '''

    help = 'List users created over REST API by a specific creator'

    def add_arguments(self, parser):
        '''
        Should receive positional argument: (creator)
        '''
        parser.add_argument('creator', nargs='?', type=str)
    
    def handle(self, **kwargs):
        '''List users created by a (creator)'''

        creator = kwargs.get('creator', None)
        # check if username has been provided
        if creator:
            # retrieve the creator user object
                creator_user = User.objects.filter(username=creator)
                if not creator_user:
                    print('\nCreator username: \'{}\' does not exist'.format(creator))
                else:
                    # get all user profiles created by creator
                    created_users = UserProfile.objects.filter(creator=creator).all()
                    if created_users:
                        print('\n\n LIST OF USERS\n')
                        for user in created_users:
                            print('User \'{}\' was created by\'{}\''.format(user.user.username, creator) )
                        print('\n')
                    else:
                        print('\nThis creator: \'{}\' has not created any users yet.\n'.format(creator))
        else:
            print("\nYou have to provide a username for the creator.")
