from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.contrib.auth.models import User
from ..forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect


def redirection(request):
    get_user = get_object_or_404(UserExtended, pk=request.user)
    if get_user.is_controller:
        return reverse('agency-dashboard', args=[get_user.agency.link])
    return reverse('user-dashboard', args=[get_user.agency.link])


""" if user is not recognized or not authenticated """


def manual_registration(request):
    form = RegisteringUser()
    e_form = UserExtendedForm()

    if request.method == 'POST':
        form = RegisteringUser(request.POST or None, request.FILES or None)
        e_form = UserExtendedForm(request.POST or None, request.FILES or None)
        if form.is_valid() and e_form.is_valid():
            user = form.save()
            e_form.save(commit=False)
            e_form.instance.user = user

        else:
            form = RegisteringUser(request.POST or None, request.FILES or None)
            e_form = UserExtendedForm(request.POST or None, request.FILES or None)

    context = {
        'form': form,
        'e_form': e_form
    }

    return render(request, '', context)


class CreateAgency(CreateView):
    model = AgencyName
    form_class = AgencyRegistering
    query_pk_and_slug = True
    slug_field = 'link'
    slug_url_kwarg = 'link'

    def get_success_url(self):
        return reverse('')

    def form_valid(self, form):
        user = self.request.user
        rs = get_object_or_404(User, pk=user.pk)
        get_user = get_object_or_404(UserExtended, user=user)
        get_user.is_controller = True
        get_user.create_access = True
        get_user.save()
        rs.save()
        return super(CreateAgency, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        return super(CreateAgency, self).dispatch(request, *args, **kwargs)
