from django.shortcuts import render


# The next lines are only used to see how the base HTML looks like
def base_screen(request):
    return render(request, 'layouts/base-app-pages.html', {
        'user_name': "User",
        'title': 'Main page',
    })


def request_classroom(request):
    return render(request, 'request-classroom.html')
