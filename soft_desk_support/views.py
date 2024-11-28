from django.http import JsonResponse

def api_home(request):
    return JsonResponse({
        "message": "Bienvenue sur l'API SoftDesk.",
        "endpoints": {
            "users": "/api/users/",
            "projects": "/api/projects/",
        }
    })