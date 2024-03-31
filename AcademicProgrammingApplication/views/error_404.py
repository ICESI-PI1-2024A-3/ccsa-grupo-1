from django.shortcuts import render


def error_404(request, exception):
    """
    Renders a custom 404 error page.

    Parameters:
        request (HttpRequest): The HTTP request object.
        exception: The exception that triggered the 404 error.

    Returns:
        HttpResponse: Rendered HTML page for the custom 404 error.
    """
    return render(request, 'error-404.html', {
        'user': request.user,
    }, status=404)
