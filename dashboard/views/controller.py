import datetime

from .main import *


class DashboardView(TemplateView):
    template_name = 'agc/main.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        agency = get_object_or_404(AgencyName, link=self.kwargs['link'])
        all_emp = UserExtended.objects.filter(agency=agency)
        all_qr = QRCodeGenerator.objects.all()

        context['QR'] = all_qr
        context['agc'] = self.kwargs['link']
        context['emp'] = all_emp.count()
        context['emp_data'] = all_emp
        return context


def registering_user(request, link):
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
            e_form.instance.is_controller = True
            e_form.instance.create_access = True
            e_form.instance.agency = link
            e_form.save()

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, '', context)


class CreateQRCode(CreateView):
    model = QRCodeGenerator
    template_name = 'main/forms.html'
    form_class = GenerateQRCodeForms
    slug_field = 'link'
    slug_url_kwarg = 'link'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('dash:agency-dashboard', args=[self.kwargs['link']])

    def form_valid(self, form):
        user = self.request.user
        valid_until = timezone.now() + datetime.timedelta(1)
        code = generate_qr_code()
        all_data = QRCodeGenerator.objects.all()
        qr_data = [x.qr_code for x in all_data]
        while True:
            if code in qr_data:
                code = generate_qr_code()
            else:
                break

        agency = get_object_or_404(AgencyName, link=self.kwargs['link'])
        form.instance.qr_code = code
        form.instance.agency = agency
        form.instance.valid_until = valid_until
        form.instance.creator = user
        return super(CreateQRCode, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateQRCode, self).dispatch(request, *args, **kwargs)
