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
    if request.GET:
        link = request.GET.get('link')
        link = InvitationLink.objects.filter(link=link)
        if not link:
            return redirect('dash:landing')
        link = get_object_or_404(InvitationLink, link=link)
        return reverse('dash:invitation', args=[link.link])

    if request.user.is_authenticated:
        get_user = UserExtended.objects.filter(user=request.user)
        if not get_user:
            return HttpResponseRedirect(reverse('dash:landing'))
        get_user = get_object_or_404(UserExtended, user=request.user)

        if get_user.agency:
            if get_user.is_controller:
                return HttpResponseRedirect(reverse('dash:agency-dashboard', args=[get_user.agency.link]))
            return HttpResponseRedirect(reverse('dash:user-dashboard', args=[get_user.agency.link]))
        return redirect('/landfed')
    return redirect('dash:landing')


""" if user is not recognized or not authenticated """


def register_by_invitation(request, link):
    is_manual = False
    form = RegisteringUser()
    e_form = UserExtendedForm()
    invitation = InvitationLink.objects.filter(link=link)
    if not invitation:
        messages.warning(request, "The link is invalid or Broken! ")
        return redirect('dash:landing')

    invitation = get_object_or_404(InvitationLink, link=link)
    time_now = pytz.utc.localize(datetime.datetime.now())
    if time_now > invitation.valid_until:
        messages.warning(request, "Maaf Forms sudah tidak menerima respons lagi")
        return redirect('dash:landing')

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
        phone = request.POST.get('phone_number')
        id_number = request.POST.get('identity_number')
        if password1 == password2:
            if form.is_valid() and e_form.is_valid():
                user = User.objects.create_user(username=username, password=password2)
                user.email = email
                user.first_name = f_name
                user.last_name = l_name
                agency = AgencyName.objects.filter(unique_code=agency_code)
                user.save()
                user = User.objects.all().order_by('-pk').first()
                e_form.instance.user__id = user.id
                e_form.instance.phone_number = phone
                e_form.instance.identity_number = id_number
                if agency:
                    agency = get_object_or_404(AgencyName, unique_code=agency_code)
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
    template_name = 'main/agency_forms.html'

    def get_success_url(self):
        return reverse('dash:agency-dashboard', args=[self.form_valid().link])

    def form_valid(self, form):
        user = self.request.user
        get_user = get_object_or_404(UserExtended, user=user)
        get_user.is_controller = True
        get_user.create_access = True

        bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
        link = form.cleaned_data['name']
        link = link.replace(' ', '-')

        for x in bad_chars:
            if bad_chars[-3] in link:
                link = link.replace(x, 'n')
            elif x in link:
                link = link.replace(x, '')

        while True:
            if link[-1] == '-':
                link = link[:-1]
            else:
                break

        form.instance.unique_code = generate_agency_code()
        form.instance.link = link
        # get_user.save()
        return super(CreateAgency, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(is_registered())
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAgency, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login')
@is_registered()
def create_agency_view(request):
    form = AgencyRegistering()
    template = 'main/agency_forms.html'
    if request.method == 'POST':
        form = AgencyRegistering(request.POST or None, request.FILES or None)
        user = get_object_or_404(UserExtended, user=request.user)
        if form.is_valid():
            bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
            link = form.cleaned_data['name']
            link = link.replace(' ', '-')

            if bad_chars[-3] in link:
                link = link.replace(bad_chars[-3], 'n')

            for x in bad_chars:
                if x in link:
                    link = link.replace(x, '-')

            while True:
                if link[-1] == '-':
                    link = link[:-1]
                else:
                    break

            name = request.POST.get('name')
            img = form.cleaned_data['img']
            desc = form.cleaned_data['desc']

            agency = AgencyName.objects.create(name=name, desc=desc)
            agency.img = img
            agency.unique_code = generate_agency_code()
            agency.link = link
            agency.save()

            user.is_controller = True
            user.create_access = True
            user.agency = agency
            user.save()
            return HttpResponseRedirect(reverse('dash:agency-dashboard', kwargs={'link': link}))

    context = {
        'form': form
    }
    return render(request, template, context)

