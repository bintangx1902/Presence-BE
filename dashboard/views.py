from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect


class DashboardView(TemplateView):
    template_name = ''


def registering_user(request):
    form = RegisteringUser()
    e_form = UserExtendedForm()
    if request.method == 'POST':
        form = RegisteringUser(request.POST or None)
        e_form = UserExtendedForm(request.POST or None)
        if form.is_valid() and e_form.is_valid():
            user = User.objects.create_user()
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.password = request.POST.get('password')
            user.first_name = request.POST.get('f_name')
            user.last_name = request.POST.get('l_name')
            user.save()
            e_form.instance.user = user
            e_form.instance.agency = request

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, '', context)


class RegisterAgency(CreateView):
    model = AgencyName
    template_name = ''
    form_class = AgencyRegistering

    def get_success_url(self):
        return reverse('')

    def form_valid(self, form):
        get_user = get_object_or_404(UserExtended, pk=get_object_or_404(User, pk=self.request.user.pk))
        get_user.is_controller = True
        get_user.save()
        return super(RegisterAgency, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterAgency, self).dispatch(request, *args, **kwargs)


def presence(request, link, pk):
    this_pre = get_object_or_404(QRCodeGenerator, pk=pk)
    this_agency = get_object_or_404(AgencyName, link=link)

    if request.method == 'POST':
        if this_pre and this_agency:
            this_pre.presence.add(request.user)

    return redirect('')


class ScanQRCode(UpdateView):
    model = QRCodeGenerator
    template_name = ''
    form_class = None
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'

    def get_qr(self):
        return get_object_or_404(QRCodeGenerator, pk=self.kwargs['pk'])

    def form_valid(self, form):
        get_qr = self.get_qr()
        user = self.request.user
        the_code = self.request.POST.get('the_code')
        if the_code and the_code == get_qr.qr_code:
            form.instance.presence = user.pk
        return super(ScanQRCode, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        get_qr = self.get_qr()
        user = self.request.user
        is_presence = get_qr.presence.filter(id=user.pk)
        if is_presence.exists():
            return HttpResponseRedirect(reverse(''))
        return super(ScanQRCode, self).dispatch(request, *args, **kwargs)


def scan(request, pk):
    get_qr = get_object_or_404(QRCodeGenerator, pk=pk)
    user = request.user
    is_presence = get_qr.presence.filter(id=user.pk)
    if request.method == 'POST':
        if is_presence.exists():
            return redirect('')
        the_code = request.POST.get('the_code')
        if the_code and the_code == get_qr.qr_code:
            get_qr.presence.add(user)

    return
