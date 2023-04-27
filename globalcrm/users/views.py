from .forms import CreationForm, RegisterUserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    

    def form_valid(self, form):
        print('form is valid')
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        print("Form is invalid!")
        return super().form_invalid(form)

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('tasks:index')
    template_name = 'users/login.html'



