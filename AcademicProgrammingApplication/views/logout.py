from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout


def logout(request):
    """
    Logs out the user and redirects to the login page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the login page.
    """
    # Log out the user
    auth_logout(request)
    # Redirect to the login page
    return redirect('login')
