from django.shortcuts import render
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Event
from .models import EventForm

@login_required
def index(request):
    """\
    The timeline with events. Login is required.
    """
    events = Event.objects.all().order_by("created_at").reverse()
    user = request.user
    return render(request, 'timeline/index.html', {'events': events, 'user': user})

@login_required
def add(request):
    """\
    Allows the user to add new events. Login is required
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_instance = Event(**form.cleaned_data)
            event_instance.user = request.user
            event_instance.save()
            return HttpResponseRedirect(reverse("events"))
        else:
            context = {"form": form}
            return render(request, 'timeline/add.html', context)
    else:
        form = EventForm(initial={'activity': 'Bouldern'})
        context = {"form": form}
        return render(request, 'timeline/add.html', context)

def about(request):
    """\
    Renders the about page.
    """
    return render(request, 'timeline/about.html')
