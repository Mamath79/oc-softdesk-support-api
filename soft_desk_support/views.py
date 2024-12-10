from django.http import JsonResponse

def api_home(request):
    """
    Documentation simplifiée de l'API SoftDesk.
    """
    return JsonResponse({
        "message": "Bienvenue sur l'API SoftDesk.",
        "description": "SoftDesk est une API RESTful pour gérer des projets, des problèmes (issues) et des commentaires.",
        "usage": "Utilisez les points d'entrée ci-dessous avec des outils comme Postman ou cURL pour interagir avec l'API.",
        "endpoints": {
            "auth": {
                "register": "/api/users/register/",
                "get_token": "/api/token/",
                "refresh_token": "/api/token/refresh/",
            },
            "users": "/api/users/",
            "projects": {
                "list_create": "/api/projects/",
                "retrieve_update_delete": "/api/projects/<project_id>/",
                "contributors": "/api/projects/<project_id>/contributors/",
                "issues": {
                    "list_create": "/api/projects/<project_id>/issues/",
                    "retrieve_update_delete": "/api/projects/<project_id>/issues/<issue_id>/",
                    "comments": {
                        "list_create": "/api/projects/<project_id>/issues/<issue_id>/comments/",
                        "retrieve_update_delete": "/api/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/"
                    }
                }
            }
        }
    }, json_dumps_params={'indent': 4})