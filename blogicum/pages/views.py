from django.shortcuts import render


def about(request):
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    template = 'pages/rules.html'
    return render(request, template)


def custom_permission_denied(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def custom_page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def custom_server_error(request):
    return render(request, 'pages/500.html', status=500)
