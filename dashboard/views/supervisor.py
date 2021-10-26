from .main import *


class DashboardView(TemplateView):
    template_name = ''


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


