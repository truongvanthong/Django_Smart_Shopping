from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
   return render(request, 'home.html')

def contact(request):
   return render(request, 'contact.html')

def error(request, exception):
   return render(request, 'error.html', {'message': exception})

def test(request):
   return render(request, 'test.html')

def support(request):
   return render(request, 'support.html')

def privacy(request):
   return render(request, 'privacy.html')

def terms(request):
   return render(request, 'terms.html')