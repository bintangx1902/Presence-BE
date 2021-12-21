from .main import *


class UserPresenceLanding(TemplateView):
    template_name = 'p/landing.html'


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
