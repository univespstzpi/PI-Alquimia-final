from django.shortcuts import render
from django.views import View

# Create your views here.
class Home(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'vitrine/home.html')