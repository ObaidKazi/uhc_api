from api.root_app import views as index_views
from api.uhc import views as uhc_views
routes_path = [
    index_views.index_routes,
    uhc_views.uhc_route
]