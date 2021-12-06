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
from ..utils import *
from django.utils import timezone

"""
Main part is for unknown user, create invitation, fill form
"""


def redirection(request):
    if request.user.is_authenticated:
        get_user = UserExtended.objects.filter(user=request.user)
        if not get_user:
            return HttpResponseRedirect(reverse('dash:landing'))
        get_user = get_object_or_404(UserExtended, user=request.user)

        if get_user.is_controller:
            return HttpResponseRedirect(reverse('dash:agency-dashboard', args=[get_user.agency.link]))
        return HttpResponseRedirect(reverse('dash:user-dashboard', args=[get_user.agency.link]))
    return redirect('dash:landing')


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
        form = RegisteringUser(request.POST or None, request.FILES or None)
        e_form = UserExtendedForm(request.POST or None, request.FILES or None)
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


def account_register(request):
    code_only = False
    form = RegisteringUser()
    e_form = UserExtendedForm()
    plus_code = False

    join = request.GET.get('join')
    if join == 'true':
        plus_code = True

    if request.user.is_authenticated:
        code_only = True
        user = UserExtended.objects.filter(user=request.user)
        if user:
            user = get_object_or_404(UserExtended, user=request.user)
            if request.method == 'POST':
                code = request.POST.get('code')
                find_agency = AgencyName.objects.filter(unique_code=code)
                if find_agency:
                    find_agency = get_object_or_404(AgencyName, unique_code=code)
                    if not user.agency == find_agency:
                        user.agency = find_agency
                        user.save()
                        return redirect('/')
                    messages.info(request, "You've been registered into agency or school!")
                    return redirect('/landed')
        return render(request, 'main/forms.html', {'code_only': code_only})

    if request.method == 'POST':
        form = RegisteringUser(request.POST or None, request.FILES or None)
        e_form = UserExtendedForm(request.POST or None, request.FILES or None)
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
                agency = AgencyName.objects.filter(unique_code=agency_code)
                if agency:
                    user.save()
                    agency = get_object_or_404(AgencyName, unique_code=agency_code)
                    e_form.instance.user = user
                    e_form.instance.agency = agency
                    e_form.save()
                    return redirect('/accounts/login/')
        messages.warning(request, "Pastikan bahwa password harus sama ! ")
    context = {
        'form': form,
        'e_form': e_form,
        'code_only': code_only,
        'pc': plus_code
    }
    return render(request, 'main/forms.html', context)


class LandingPage(TemplateView):
    template_name = 'main/landing.html'

    def dispatch(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse('dash:main'))
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
