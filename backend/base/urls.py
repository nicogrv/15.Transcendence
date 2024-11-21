
from django.urls import path
from django.shortcuts import render

def index(request, pk=None):
    uuid_from_query = request.GET.get('id', None)
    if uuid_from_query:
        # Process the UUID, e.g., fetch data related to the UUID
        # For demonstration, we'll just echo the UUID back to the template
        context = {'uuid': uuid_from_query}
    else:
        # Handle the case where no UUID is provided
        context = {}
        pass
    return render(request, "index.html", context)


urlpatterns = [
    path('friendsList', index, name='index'),
    path('settings', index, name='index'),
    path('account', index, name='index'),
    path('signUp', index, name='index'),
    path('signIn', index, name='index'),
	path('', index, name='index'),
    path('pong?id=<uuid:pk>', index, name='index'),
    path('pong', index, name='index'),
    path('userProfile/<uuid:pk>', index, name='index'),
    path('tournament', index, name='index'),
    path('tournament/<uuid:pk>', index, name="index"),
	path('search', index, name='index'),
]

# Catch-all route for SPA
# urlpatterns += [
#     re_path(r'^.*$', TemplateView.as_view(template_name="index.html"), name='spa'),
# ]