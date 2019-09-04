

from django.shortcuts import render

from .google_sheets_api import log_in, get_spreadsheet

def index(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)


def schedule(request):
    template = 'schedule.html'
    context = {}
    return render(request, template, context)


def signup(request):
    service = log_in()
    spreadsheet = get_spreadsheet(service)

    attendees = [row[0] for row in spreadsheet['values'] if row[0] != '']

    template = 'signup.html'
    context = {'attendees': attendees}
    return render(request, template, context)
