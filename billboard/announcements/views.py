from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AnnouncementForm, CommentForm
from .models import Announcement, Author, Comment


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-add_date'
    template_name = 'announcements.html'
    context_object_name = 'announcements'
    paginate_by = 10


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'


class AnnouncementCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('announcements.add_announcement',)
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Adding current user to the form
        if not Author.objects.filter(author=self.request.user).exists():
            Author.objects.create(author=self.request.user)
        self.object.author = Author.objects.get(author=self.request.user)
        self.object.save()
        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('announcements.change_announcement',)
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement_edit.html'

    def get_object(self, queryset=None):
        obj = UpdateView.get_object(self, queryset=None)
        if not obj.author.author == self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Adding current user to the form
        self.object.author = Author.objects.get(author=self.request.user)
        self.object.save()
        return super().form_valid(form)


class AnnouncementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('announcements.delete_announcement',)
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcements')


@login_required
def comments_list(request):
    announcements = Announcement.objects.filter(author__author=request.user).order_by('-add_date')
    context = {
        'announcements': announcements
    }
    return render(request, 'comments.html', context)


def comment_create(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user.is_authenticated and announcement.author.author != request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.announcement = announcement
                comment.save()

                current_site = get_current_site(request)
                mail_subject = 'Your announcement has been commented'
                message = render_to_string('comment_create_email.html', {
                    'user': request.user,
                    'link': f'http://{current_site.domain}/announcements/',
                    'announcement': announcement,
                })
                to_email = announcement.author.author.email
                email = EmailMessage(
                    mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email]
                )
                email.send()

                return redirect('announcement', pk)
        else:
            form = CommentForm()
    else:
        raise PermissionDenied()
    return render(request, 'comment_edit.html', {'form': form})


def comment_approve(request, pk1, pk2):
    announcement = get_object_or_404(Announcement, pk=pk1)
    comment = get_object_or_404(Comment, pk=pk2)
    if announcement.author.author == request.user or request.user.is_staff:
        comment.is_new = False
        comment.save()

        current_site = get_current_site(request)
        mail_subject = 'Your comment has been approved by announcement author'
        message = render_to_string('comment_approve_email.html', {
            'user': request.user,
            'link': f'http://{current_site.domain}/announcements/',
            'announcement': announcement,
            'comment': comment,
        })
        to_email = comment.author.email
        email = EmailMessage(
            mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email]
        )
        email.send()

        return redirect('comments')
    else:
        raise PermissionDenied()


def comment_update(request, pk1, pk2):
    comment = get_object_or_404(Comment, pk=pk2)
    if request.user.is_authenticated and (comment.author == request.user or request.user.is_staff):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form_data = request.POST.dict()
                comment.text = form_data.get('text')
                comment.save()
                return redirect('announcement', pk1)
        else:
            form = CommentForm(instance=comment)
    else:
        raise PermissionDenied()
    return render(request, 'comment_edit.html', {'form': form})


def comment_delete(request, pk1, pk2):
    announcement = get_object_or_404(Announcement, pk=pk1)
    comment = get_object_or_404(Comment, pk=pk2)
    if comment.author == request.user or announcement.author.author == request.user or request.user.is_staff:
        if request.method == 'POST':
            comment.delete()
            return redirect('announcement', pk1)
        else:
            return render(request, 'comment_delete.html')
    else:
        raise PermissionDenied()
