from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from .models import LostItem, Location, FoundItem, Hub
from .forms import LostItemForm, FoundItemForm, HubForm
from django.utils import timezone
import json
import html


# Create your views here.
def index(request):
    lost_item_list = LostItem.objects.filter(sub_date__lte=timezone.now()).order_by("-sub_date")[:5]
    found_item_list = FoundItem.objects.filter(found_date__lte=timezone.now()).order_by("-found_date")[:5]
    show_hub_alert = request.GET.get('show_hub_alert')
    show_found_alert = request.GET.get('show_found_alert')
    show_lost_alert = request.GET.get('show_lost_alert')
    if request.user.is_authenticated:
        return render(request, 'home/index.html',
                      {'lost_item_list': lost_item_list,
                       'found_item_list': found_item_list,
                       'show_hub_alert': show_hub_alert,
                       'show_found_alert': show_found_alert,
                       'show_lost_alert': show_lost_alert,
                       })
    else:
        # return HttpResponseRedirect(reverse("login:login", ))
        return render(request, 'home/index-logged-out.html',
                      {'lost_item_list': lost_item_list, 'found_item_list': found_item_list})


def lost_items(request):
    if request.user.is_authenticated:
        lost_item_list = LostItem.objects.filter(sub_date__lte=timezone.now()).order_by("-sub_date")
        return render(request, 'home/lost-items.html', {'lost_item_list': lost_item_list}, )
    else:
        return HttpResponseRedirect(reverse("login:login", ))


def found_items(request):
    if request.user.is_authenticated:
        found_item_list = FoundItem.objects.filter(found_date__lte=timezone.now()).order_by("-found_date")
        return render(request, 'home/found-items.html', {'found_item_list': found_item_list}, )
    else:
        return HttpResponseRedirect(reverse("login:login", ))


def hubs(request):
    if request.user.is_authenticated:
        hubs = Hub.objects.filter(approved=True)
        found_item_list = FoundItem.objects.filter(found_date__lte=timezone.now()).order_by("-found_date")
        return render(request, 'home/hubs.html', {'found_item_list': found_item_list, 'hubs': hubs}, )
    else:
        return HttpResponseRedirect(reverse("login:login", ))


# Source: https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/
def lost_item_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            lost_form = LostItemForm(request.POST)
            if lost_form.is_valid():
                temp = lost_form.save(False)
                temp.user = request.user

                latitude = request.POST['latitude']
                longitude = request.POST['longitude']
                location = Location(latitude=latitude, longitude=longitude)
                location.save()
                show_lost_alert = True

                temp.location = location
                temp.save()
                return HttpResponseRedirect(reverse("home:index") + f'?show_lost_alert={show_lost_alert}')
        else:
            lost_form = LostItemForm()
        return render(request, "home/lost-form.html", {"lost_item_form": lost_form})
    else:
        return HttpResponseRedirect(reverse("login:login", ))


def found_item_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            found_form = FoundItemForm(request.POST)
            if found_form.is_valid():
                temp = found_form.save(False)
                temp.user = request.user

                latitude = request.POST['latitude']
                longitude = request.POST['longitude']
                location = Location(latitude=latitude, longitude=longitude)
                location.save()
                show_found_alert = True

                temp.location = location
                hub = request.POST['hub']

                if hub:
                    temp.hub = get_object_or_404(Hub, pk=hub)

                temp.save()
                return HttpResponseRedirect(reverse("home:index") + f'?show_found_alert={show_found_alert}')
        else:
            found_form = FoundItemForm()
            hubs = Hub.objects.filter(approved=True)
            hubsJson = []

            # source for html.escape: https://www.educative.io/answers/what-is-htmlescape-in-python
            # prevents issues if there are ' " < > etc in the name/description
            for hub in hubs:
                hubJson = {
                    "name": html.escape(hub.name),
                    "description": html.escape(hub.description),
                    "lat": str(hub.location.latitude),
                    "long": str(hub.location.longitude)
                }
                hubsJson.append(hubJson)
            jsonstring = json.dumps(hubsJson)
            jsonstring = jsonstring.replace("\\r\\n", "<br>")
        return render(request, "home/found-form.html",
                      {"found_item_form": found_form, 'hubs': hubs, 'hubsJson': jsonstring})
    else:
        return HttpResponseRedirect(reverse("login:login", ))


def hub_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            hub_form = HubForm(request.POST)
            if hub_form.is_valid():
                temp = hub_form.save(False)
                show_hub_alert = True

                latitude = request.POST['latitude']
                longitude = request.POST['longitude']
                location = Location(latitude=latitude, longitude=longitude)
                location.save()

                temp.location = location

                temp.save()
                return HttpResponseRedirect(reverse("home:index") + f'?show_hub_alert={show_hub_alert}')
        else:
            hub_form = HubForm()
        return render(request, "home/hub-form.html", {"hub_form": hub_form})
    else:
        return HttpResponseRedirect(reverse("login:login"))


def approve_hubs(request):
    if request.user.is_staff:
        submitted_hubs = Hub.objects.filter(approved=False)
        return render(request, "home/approve-hubs.html", {"submitted_hubs": submitted_hubs})
    else:
        return redirect("home:index")


def approve_hub(request, hub):
    if request.user.is_staff:
        hubToApprove = get_object_or_404(Hub, pk=hub)
        hubToApprove.approved = True
        hubToApprove.save()
    return HttpResponseRedirect(reverse("home:index"))


def lost_detail(request, pk):
    # Initialize lost_item to None
    lost_item = None

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve the LostItem object with the given primary key (pk)
        lost_item = get_object_or_404(LostItem, pk=pk)

        # Initialize the context dictionary
        context = {'lost_item': lost_item, 'owned_by_you': True}

        # Check if the request method is POST and if the 'delete' button is clicked
        if request.method == 'POST' and 'delete' in request.POST:
            # Check if the logged-in user is the owner of the lost item
            if request.user.email == lost_item.user.email:
                # Handle item deletion here
                lost_item.delete()
                return HttpResponseRedirect(reverse("home:index"))

            # If the user is not the owner, set show_word to True
            context['owned_by_you'] = False

        # Render the template with the context
        return render(request, 'home/lost-item-detail.html', context)

    else:
        # Redirect to the home:index page if the user is not authenticated
        return HttpResponseRedirect(reverse("home:index"))


def found_detail(request, pk):
    if request.user.is_authenticated:
        found_item = get_object_or_404(FoundItem, pk=pk)
        # Check if a delete request has been sent via POST
        if request.method == 'POST' and 'delete' in request.POST:
            # Handle item deletion here
            found_item.delete()
            return HttpResponseRedirect(reverse("home:index"))
        if found_item.hub:
            hubJson = {
                "name": html.escape(found_item.hub.name),
                "description": html.escape(found_item.hub.description),
                "lat": str(found_item.hub.location.latitude),
                "long": str(found_item.hub.location.longitude)
            }
        else:
            hubJson = {}
        jsonstring = json.dumps(hubJson).replace("\\r\\n", "<br>")
        return render(request, 'home/found-item-detail.html', {'found_item': found_item, 'hubsJson':jsonstring})
    else:
        return HttpResponseRedirect(reverse("home:index"))


def claimed_item(request, pk):
    if request.user.is_authenticated:
        found_item = get_object_or_404(FoundItem, pk=pk)

        # Check if a delete request has been sent via POST
        if request.method == 'POST' and 'delete' in request.POST:
            # Handle item deletion here
            found_item.delete()
            return HttpResponseRedirect(reverse("home:index"))

        return render(request, 'home/claimed-item.html', {'found_item': found_item})
    else:
        return HttpResponseRedirect(reverse("home:index"))


class HubDetailView(DetailView):
    model = Hub
    template_name = 'home/hub-detail.html'
    context_object_name = 'hub'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['found_items'] = FoundItem.objects.filter(hub=self.object)
        return context
