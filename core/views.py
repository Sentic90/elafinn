from django.shortcuts import render

# Create your views here.
def custom_404(request, exception=None):
    return render(request, 'core/404.html', status=404)