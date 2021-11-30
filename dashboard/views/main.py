import datetime, pytz
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.contrib.auth.models import User
from ..forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from ..utils import generate_agency_code

"""
Main part is for unknown user, create invitation, fill form
"""


@login_required(login_url='/accounts/login')
def redirection(request):
    try:
        get_user = UserExtended.objects.get(user__id=request.user.id)
    except UserExtended.DoesNotExist:
        return redirect('dash:agency')

    if get_user.is_controller:
        return reverse('agency-dashboard', args=[get_user.agency.link])
    return reverse('user-dashboard', args=[get_user.agency.link])


""" if user is not recognized or not authenticated """


def register_by_invitation(request, link):
    is_manual = False
    form = RegisteringUser()
    e_form = UserExtendedForm()
    invitation = InvitationLink.objects.filter(link=link)
    if not invitation:
        return redirect

    invitation = get_object_or_404(InvitationLink, link=link)
    time_now = pytz.utc.localize(datetime.datetime.now())
    if time_now <= invitation.valid_until:
        messages.warning(request, "Maaf Forms ini sudah tidak menerima respons lagi")

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if form.is_valid() and e_form.is_valid():
                user = User.objects.create_user(usernname=username, password=password2)
                user.first_name = f_name
                user.last_name = l_name
                user.email = email
                user.save()
                e_form.instance.user = user
                e_form.instance.agency = invitation.agency
                e_form.save()
                return reverse

        messages.warning(request, "Pastikan Password harus sama! ")

    context = {
        'form': form,
        'e_form': e_form,
        'is_manual': is_manual
    }

    return render(request, 'main/forms.html', context)


def manual_registration(request):
    is_manual = True
    form = RegisteringUser()
    e_form = UserExtendedForm()

    if request.method == 'POST':
        agency_code = request.POST.get('code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        username = request.POST.get('username')
        if password1 == password2:
            if form.is_valid() and e_form.is_valid():
                user = User.objects.create_user(username=username, password=password2)
                user.email = email
                user.first_name = f_name
                user.last_name = l_name
                # user.save()
                agency = get_object_or_404(AgencyName, code=agency_code)
                e_form.instance.user = user
                e_form.instance.agency = agency
                # e_form.save()
                # return reverse
        # messages.warning(request, "Pastikan bahwa password harus sama ! ")
    context = {
        'form': form,
        'e_form': e_form,
        'is_manual': is_manual
    }
    return render(request, 'main/forms.html', context)


def account_register(request):
    is_manual = False
    form = RegisteringUser()
    e_form = UserExtendedForm()

    if request.method == 'POST':
        agency_code = request.POST.get('code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        username = request.POST.get('username')
        if password1 == password2:
            if form.is_valid() and e_form.is_valid():
                user = User.objects.create_user(username=username, password=password2)
                user.email = email
                user.first_name = f_name
                user.last_name = l_name
                # user.save()
                agency = get_object_or_404(AgencyName, code=agency_code)
                e_form.instance.user = user
                e_form.instance.agency = agency
                # e_form.save()
                # return reverse
        # messages.warning(request, "Pastikan bahwa password harus sama ! ")
    context = {
        'form': form,
        'e_form': e_form,
        'is_manual': is_manual
    }
    return render(request, 'main/forms.html', context)


class LandingPage(TemplateView):
    template_name = 'main/landing.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LandingPage, self).dispatch(request, *args, **kwargs)


class CreateAgency(CreateView):
    model = AgencyName
    form_class = AgencyRegistering
    query_pk_and_slug = True
    slug_field = 'link'
    slug_url_kwarg = 'link'
    template_name = 'main/agency_forms.html'

    def get_success_url(self):
        return reverse('')

    def form_valid(self, form):
        user = self.request.user
        get_user = get_object_or_404(UserExtended, user=user)
        get_user.is_controller = True
        get_user.create_access = True
        form.instance.link = generate_agency_code()
        get_user.save()
        return super(CreateAgency, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAgency, self).dispatch(request, *args, **kwargs)



