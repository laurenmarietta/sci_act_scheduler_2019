

from django.shortcuts import render

from . import google_sheets_api
from .forms import GetAttendeeAvailability

def index(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)


def schedule(request):
    template = 'schedule.html'
    context = {}
    return render(request, template, context)


def signup(request):
    service = google_sheets_api.log_in()
    df = google_sheets_api.get_dataframe(service)

    attendees = df.iloc[:,0]

    availability_table = ''
    show_table = False

    # Create a form instance and populate it with data from the request
    form = GetAttendeeAvailability(request.POST or None)

    # If this is a POST request, we need to process the form data
    if request.method == 'POST':
        if form.is_valid():
            availability_table = form.get_availability()
            show_table = True

    template = 'signup.html'
    context = {'attendees': attendees,
               'form': form,
               'show_table': show_table,
               'availability_table': availability_table}
    return render(request, template, context)
