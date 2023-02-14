from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save form in the memory (not in database)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('registration/signup_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email]
            )
            email.send()
            return render(request, 'registration/signup_confirm_notice.html')
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        for user in User.objects.all():
            if not user.is_active:
                user.delete()
        return render(request, 'registration/signup_failed.html')
    difference = datetime.now(user.date_joined.tzinfo) - user.date_joined
    if account_activation_token.check_token(user, token) and difference.total_seconds() < 300:
        group = Group.objects.get(name='authors')
        user.is_active = True
        user.groups.add(group)
        user.save()
        login(request, user)
        return render(request, 'registration/signup_success.html')
    else:
        user.delete()
        return render(request, 'registration/signup_failed.html')
