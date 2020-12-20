
from urllib.parse import urljoin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.forms import (
    MyLoginForm, MyUserCreationForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm,
    UserUpdateForm
)
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import redirect, resolve_url
from django.core.signing import SignatureExpired, BadSignature, loads, dumps
from django.http import HttpResponseBadRequest
from .models import User, Group


class Login(LoginView):
    form_class = MyLoginForm
    template_name = 'accounts/login.html'


class Logout(LogoutView):
    template_name = 'accounts/logout.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'accounts/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string(
            'accounts/mail_template/email_change/subject.txt',
            context
        )
        message = render_to_string(
            'accounts/mail_template/email_change/message.txt',
            context
        )
        send_mail(subject, message, None, [new_email])

        return redirect('accounts:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'accounts/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'accounts/email_change_complete.html'
    # デフォルトでは1日以内
    timeout_seconds = getattr(
        settings,
        'ACTIVATION_TIMEOUT_SECONDS',
        60 * 60 * 24
    )

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            print('Bad token')
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class OnlyNotMemberMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        try:
            return not bool(self.request.user.group)
        except AttributeError:
            return True


class OnlyMemberMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user in self.request.user.group.users.all()


class OnlyOwnerMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user == self.request.user.group.owner


class GroupCreateView(OnlyNotMemberMixin, generic.CreateView):
    model = Group

    fields = ('name',)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        self.request.user.group = self.object
        self.request.user.save()
        return reverse(
            'accounts:user_detail',
            kwargs=dict(pk=self.request.user.pk)
        )


class GroupUpdateView(OnlyOwnerMixin, generic.UpdateView):
    model = Group

    fields = ('name',)


class GroupDetailView(OnlyMemberMixin, generic.DetailView):
    model = Group

    def post(self, request, *args, **kwargs):
        if request.POST['command'] == 'accept':
            member = User.objects.get(pk=int(request.POST['pk']))
            member.group = Group.objects.get(pk=int(kwargs['pk']))
            member.requesting_group = None
            member.save() 
            return HttpResponseRedirect(reverse('accounts:group_detail', kwargs={'pk': int(kwargs['pk'])}))
        elif request.POST['command'] == 'dissmiss':
            member = User.objects.get(pk=int(request.POST['pk']))
            member.requesting_group = None
            member.save() 
            return HttpResponseRedirect(reverse('accounts:group_detail', kwargs={'pk': int(kwargs['pk'])}))


class GroupJoinConfirmView(OnlyNotMemberMixin, generic.DetailView):
    model = Group
    template_name = 'accounts/group_join_confirm.html'

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse('accounts:group_join_request_done', kwargs={'pk': int(kwargs['pk'])})
        )


class GroupJoinDoneView(OnlyNotMemberMixin, generic.DetailView):
    model = Group
    template_name = 'accounts/group_join_done.html'


class GroupJoinInviteView(OnlyOwnerMixin, generic.DetailView):
    model = Group
    template_name = 'accounts/group_join_invite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = urljoin(
            self.request._current_scheme_host,
            reverse('accounts:group_join_confirm', kwargs={'pk': kwargs['object'].id})
        )
        context['url'] = url
        return context


class GroupJoinRequestViewView(OnlyNotMemberMixin, generic.TemplateView):
    template_name = 'accounts/group_join_request.html'


class GroupQuitConfirmView(OnlyMemberMixin, generic.DetailView):
    model = Group
    template_name = 'accounts/group_quit_confirm.html'


class GroupQuitDoneView(OnlyNotMemberMixin, generic.DetailView):
    model = Group
    template_name = 'accounts/group_quit_done.html'


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password_change_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class UserDetailView(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'accounts/user_detail.html'


class UserUpdateView(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'

    def get_success_url(self):
        return resolve_url('accounts:user_detail', pk=self.kwargs['pk'])