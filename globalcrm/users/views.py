from .models import Profile
from .forms import CreationForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from tasks.forms import TaskForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        print("form is valid")
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        print("Form is invalid!")
        return super().form_invalid(form)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("tasks:index")
    template_name = "users/login.html"


class ProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get_absolute_url(self, task):
        return reverse("tasks:task_detail", kwargs={"pk": task.pk})

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        tasks = Task.objects.filter(worker=request.user)
        form = TaskForm()
        context = {"profile": profile, "tasks": tasks, "form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.worker = request.user
            task.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


class CalendarView(LoginRequiredMixin, View):
    template_name = "users/calendar.html"

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(worker=request.user)
        return render(request, self.template_name, {"tasks": tasks})
