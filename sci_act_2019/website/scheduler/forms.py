"""Defines forms

Django allows for an object-oriented model representation of forms for
users to provide input through HTTP POST methods. This module defines
all of the forms that are used across the various webpages used for the
sci_act_2019 application.

Use
---

    This module is used within ``views.py`` as such:
    ::
        from .forms import FileSearchForm
        def view_function(request):
            form = FileSearchForm(request.POST or None)

            if request.method == 'POST':
                if form.is_valid():
                    # Process form input and redirect
                    return redirect(new_url)

            template = 'some_template.html'
            context = {'form': form, ...}
            return render(request, template, context)

References
----------
    For more information please see:
        ``https://docs.djangoproject.com/en/2.1/topics/forms/``
"""
import glob
import os

from django import forms
from django.shortcuts import redirect
import numpy as np

from .google_sheets_api import log_in, get_attendees, get_dataframe

GOOGLE_SHEETS_SERVICE = log_in()

class GetAttendeeAvailability(forms.Form):
    """Double-field form to search for a proposal or fileroot."""

    choices = [(person, person) for person in get_attendees(GOOGLE_SHEETS_SERVICE)]

    # Define user name field
    user = forms.ChoiceField(label='Who are you?', required=True,
                             choices=choices)
    # Define search field
    attendee = forms.ChoiceField(label='Who do you want to meet with?', required=True,
                                 choices=choices)

    # Initialize attributes

    def clean_user(self):
        """Validate the "user" field.

        Check that the input is either a proposal or fileroot, and one
        that matches files in the filesystem.

        Returns
        -------
        str
            The cleaned data input into the "search" field

        """
        # Get the cleaned search data
        user = self.cleaned_data['user']

        # # Make sure the search is either a proposal or fileroot
        # if len(search) == 5 and search.isnumeric():
        #     self.search_type = 'proposal'
        # elif self._search_is_fileroot(search):
        #     self.search_type = 'fileroot'
        # else:
        #     raise forms.ValidationError('Invalid search term {}. Please provide proposal number '
        #                                 'or file root.'.format(search))
        #
        # # If they searched for a proposal...
        # if self.search_type == 'proposal':
        #     # See if there are any matching proposals and, if so, what
        #     # instrument they are for
        #     search_string = os.path.join(FILESYSTEM_DIR, 'jw{}'.format(search),
        #                                  '*{}*.fits'.format(search))
        #     all_files = glob.glob(search_string)
        #     if len(all_files) > 0:
        #         all_instruments = []
        #         for file in all_files:
        #             instrument = filename_parser(file)['instrument']
        #             all_instruments.append(instrument)
        #         if len(set(all_instruments)) > 1:
        #             raise forms.ValidationError('Cannot return result for proposal with multiple '
        #                                         'instruments.')
        #
        #         self.instrument = all_instruments[0]
        #     else:
        #         raise forms.ValidationError('Proposal {} not in the filesystem.'.format(search))
        #
        # # If they searched for a fileroot...
        # elif self.search_type == 'fileroot':
        #     # See if there are any matching fileroots and, if so, what
        #     # instrument they are for
        #     search_string = os.path.join(FILESYSTEM_DIR, search[:7], '{}*.fits'.format(search))
        #     all_files = glob.glob(search_string)
        #
        #     if len(all_files) == 0:
        #         raise forms.ValidationError('Fileroot {} not in the filesystem.'.format(search))
        #
        #     instrument = search.split('_')[-1][:3]
        #     self.instrument = JWST_INSTRUMENT_NAMES_SHORTHAND[instrument]

        return self.cleaned_data['user']

    def clean_attendee(self):
        """Validate the "attendee" field.

        Check that the input is either a proposal or fileroot, and one
        that matches files in the filesystem.

        Returns
        -------
        str
            The cleaned data input into the "search" field

        """
        # Get the cleaned search data
        attendee = self.cleaned_data['attendee']

        return self.cleaned_data['attendee']


    def get_availability(self):
        # Process the data in form.cleaned_data as required
        user = self.cleaned_data['user']
        attendee = self.cleaned_data['attendee']

        df = get_dataframe(GOOGLE_SHEETS_SERVICE)
        print(df)


        available_times = (df.loc[user] == '') & (df.loc[attendee] == '')

        print(user, attendee, available_times)

        return available_times
