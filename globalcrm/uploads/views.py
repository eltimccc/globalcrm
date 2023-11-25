from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from .forms import FileUploadForm

# class FileUploadView(View):
#     form_class = FileUploadForm
#     template_name = 'uploads/upload.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('tasks:index'))
#         return render(request, self.template_name, {'form': form})


class FileUploadView(View):
    form_class = FileUploadForm
    template_name = "uploads/upload.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return render(
                request,
                self.template_name,
                {"form": form, "uploaded_file": uploaded_file},
            )
        return render(request, self.template_name, {"form": form})
