from django.shortcuts import render

def google_login_view(request):
    return render(request, 'home.html')
