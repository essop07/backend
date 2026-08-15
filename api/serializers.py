from rest_framework import serializers
from .models import Renting
from .models import ElectricityBills
from .models import OldTenants
from .models import MonthlyRent
class RentingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Renting
        fields = "__all__"
class ElectricityBillsSerializer(serializers.ModelSerializer):

    property_id = serializers.CharField(
        source="property.property_id"
    )

    tenant_name = serializers.CharField(
        source="property.temp_owner"
    )

    class Meta:
        model = ElectricityBills
        fields = [
            "property_id",
            "tenant_name",
            "year",
            "month",
            "previous_reading",
            "current_reading",
            "units_consumed",
            "rate_per_unit",
            "total_amount",
            "paid",
            "payment_date",
            "remarks",
        ]

class OldTenantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldTenants
        fields = "__all__"


class MonthlyRentSerializer(serializers.ModelSerializer):

    property_id = serializers.CharField(source="property.property_id")
    tenant_name = serializers.CharField(source="property.temp_owner")
    mob_number = serializers.CharField(source="property.mob_number")

    class Meta:
        model = MonthlyRent
        fields = [
            "property_id",
            "tenant_name",
            "mob_number",
            "year",
            "month",
            "rent_amount",
            "paid",
            "payment_date",
        ]