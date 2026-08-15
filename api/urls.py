from django.urls import path
from .views import (
    properties,
    dashboard,
    property_all,
    search_tenant,
    pay_rent,
    undo_rent,
    rent_list,
    update_property,
    add_property,
    electricity_list,
    update_electricity,
    undo_electricity,
    pay_electricity,
    old_tenants_all,
)

urlpatterns = [
    path("properties/", properties),
    path("dashboard/", dashboard),
    path("search/", search_tenant),
    path("rent/", rent_list),
    path(
    "rent/pay/<str:property_id>/<int:year>/<int:month>/",
    pay_rent,
    ),

    path(
        "rent/undo/<str:property_id>/<int:year>/<int:month>/",
        undo_rent,
    ),
    path("property/update/<str:property_id>/", update_property),
    path("property/add/", add_property),
    path("electricity/", electricity_list),

    path(
        "electricity/update/<str:property_id>/<int:year>/<int:month>/",
        update_electricity
    ),

    path(
        "electricity/pay/<str:property_id>/<int:year>/<int:month>/",
        pay_electricity
    ),

    path(
        "electricity/undo/<str:property_id>/<int:year>/<int:month>/",
        undo_electricity
    ),
    path("old-tenants/", old_tenants_all),
    path("properties/", property_all),
]