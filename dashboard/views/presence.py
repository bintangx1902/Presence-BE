from .main import *
from django.contrib import messages


class UserPresenceLanding(TemplateView):
    template_name = 'p/landing.html'

    def get_context_data(self, **kwargs):
        context = super(UserPresenceLanding, self).get_context_data(**kwargs)
        usx = get_object_or_404(UserExtended, user=self.request.user)
        history = PresenceRecap.objects.filter(user=usx)

        context['agc'] = self.kwargs['link']
        context['history'] = history
        return context


class ScanQRCode(UpdateView):
    model = QRCodeGenerator
    template_name = 'p/forms.html'
    form_class = None
    # query_pk_and_slug = True
    # slug_field = 'link'

    def form_valid(self, form):
        user = self.request.user
        return super(ScanQRCode, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # if is_presence.exists():
        #     return HttpResponseRedirect(reverse(''))
        return super(ScanQRCode, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login')
def scan(request, link):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = get_object_or_404(UserExtended, user=request.user)
        get_code = QRCodeGenerator.objects.filter(qr_code=code)
        if not get_code:
            return HttpResponseRedirect(reverse('dash:user-dashboard', args=[link]))
        get_code = get_object_or_404(QRCodeGenerator, qr_code=code)
        if get_code.agency != user.agency:
            messages.error(request, "Presence QR agency and your agency is not same! ")
            return HttpResponseRedirect(reverse('dash:user-dashboard', args=[link]))

        recapitulated = PresenceRecap.objects.filter(user=user, qr=get_code)
        if recapitulated:
            return redirect(f"/{link}/user")

        recap = PresenceRecap.objects.create(
            qr=get_code, user=user
        )
        recap.save()
        return HttpResponseRedirect(reverse('dash:user-dashboard', args=[link]))

    context = {}
    return render(request, 'p/forms.html', context)


class HistoryDetailView(DetailView):
    model = QRCodeGenerator
    template_name = 'p/hist.html'
    context_object_name = 'qr'
    # query_pk_and_slug = True
    # slug_field = 'link', 'qr'
    # slug_url_kwarg = 'link', 'qr'

    def get_object(self, queryset=None):
        return get_object_or_404(QRCodeGenerator, qr_code=self.kwargs['qr'])

    def get_context_data(self, **kwargs):
        context = super(HistoryDetailView, self).get_context_data(**kwargs)
        usx = get_object_or_404(UserExtended, user=self.request.user)
        time_stamp = get_object_or_404(PresenceRecap, qr=self.get_object(), user=usx)

        context['recap'] = time_stamp
        context['agc'] = self.kwargs['link']
        return context
