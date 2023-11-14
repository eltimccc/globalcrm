from .models import Profile
from .forms import CreationForm, RegisterUserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View


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


# @login_required
# def profile(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     return render(request, 'profile.html', {'profile': profile})


class ProfileView(View):
    template_name = "users/profile.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        context = {"profile": profile}
        return render(request, self.template_name, context)
