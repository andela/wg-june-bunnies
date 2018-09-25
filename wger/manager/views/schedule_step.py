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

import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy, ugettext as _
from django.db import models
from django.forms import ModelForm, ModelChoiceField
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView
)

from wger.manager.models import (
    Schedule,
    ScheduleStep,
    Workout
)
from wger.utils.generic_views import (
    WgerFormMixin,
    WgerDeleteMixin
)


logger = logging.getLogger(__name__)


class StepCreateView(WgerFormMixin, CreateView, PermissionRequiredMixin):
    '''
    Creates a new workout schedule
    '''

    model = ScheduleStep
    fields = '__all__'
    title = ugettext_lazy('Add workout')

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(ModelForm):
            workout = ModelChoiceField(
                queryset=Workout.objects.filter(user=self.request.user))
            
            def __init__(self, schedule_id, *args, **kwargs):
                super(StepForm, self).__init__(*args, **kwargs)
                # set the schedule_id as an attribute of the form
                self.schedule_id = schedule_id
            
            def clean_duration(self):
                """Ensures duration does not exceed period"""
                duration = self.cleaned_data['duration']
                schedule = Schedule.objects.get(pk=self.schedule_id)
                sum_duration = schedule.schedulestep_set.all().aggregate(models.Sum('duration'))
                # Catch NoneType error for 1st workout to be added to schedule.
                sum_duration = sum_duration['duration__sum'] or 0
                derived_duration = duration + sum_duration
    
                # Check if duration exceeds cycle duration
                if schedule.period == 'Macrocycle' and derived_duration > 52:
                    msg = 'Duration Cycle exceeds 1 year. \'{}\' weeks are left in the cycle'.format(52 - sum_duration)
                    raise ValidationError(_(msg))
                elif schedule.period == 'Mesocycle' and derived_duration > 6:
                    msg = 'Duration cycle excedds 6 weeks. \'{}\' weeks are left in the cycle'.format(6-sum_duration)
                    raise ValidationError(_(msg))
                elif schedule.period == 'Microcycle' and derived_duration > 1:
                    raise ValidationError(_(
                        'Workout already exists. Delete existing workout to add new one'))
                return duration

            class Meta:
                model = ScheduleStep
                exclude = ('order', 'schedule')


        return StepForm
    
    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['schedule_id'] = self.kwargs['schedule_pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('manager:step:add',
                                         kwargs={'schedule_pk': self.kwargs['schedule_pk']})
        return context

    def get_success_url(self):
        return reverse('manager:schedule:view', kwargs={'pk': self.kwargs['schedule_pk']})

    def form_valid(self, form):
        '''Set the schedule and the order'''

        schedule = Schedule.objects.get(pk=self.kwargs['schedule_pk'])

        max_order = schedule.schedulestep_set.all().aggregate(models.Max('order'))
        form.instance.schedule = schedule
        form.instance.order = (max_order['order__max'] or 0) + 1
        return super(StepCreateView, self).form_valid(form)


class StepEditView(WgerFormMixin, UpdateView, PermissionRequiredMixin):
    '''
    Generic view to update an existing schedule step
    '''

    model = ScheduleStep
    title = ugettext_lazy('Edit workout')
    form_action_urlname = 'manager:step:edit'

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(ModelForm):
            workout = ModelChoiceField(
                queryset=Workout.objects.filter(user=self.request.user))

            class Meta:
                model = ScheduleStep
                exclude = ('order', 'schedule')

        return StepForm

    def get_success_url(self):
        return reverse('manager:schedule:view', kwargs={'pk': self.object.schedule_id})


class StepDeleteView(WgerDeleteMixin, DeleteView, PermissionRequiredMixin):
    '''
    Generic view to delete a schedule step
    '''

    model = ScheduleStep
    fields = ('workout', 'duration', 'order')
    form_action_urlname = 'manager:step:delete'
    messages = ugettext_lazy('Successfully deleted')

    def get_success_url(self):
        return reverse('manager:schedule:view', kwargs={'pk': self.object.schedule.id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(StepDeleteView, self).get_context_data(**kwargs)
        context['title'] = _(u'Delete {0}?').format(self.object)
        context['form_action'] = reverse('core:license:delete', kwargs={
                                         'pk': self.kwargs['pk']})
        return context
