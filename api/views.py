from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Renting,MonthlyRent
from .serializers import RentingSerializer
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from .models import OldTenants
from .serializers import OldTenantsSerializer
from .serializers import MonthlyRentSerializer
from .models import ElectricityBills
from .serializers import ElectricityBillsSerializer

@api_view(["GET"])
def properties(request):
    properties = Renting.objects.all().order_by("property_id")
    serializer = RentingSerializer(properties, many=True)
    return Response(serializer.data)


from django.utils import timezone
from django.db.models import Q, Sum

@api_view(["GET"])
def dashboard(request):

    today = timezone.localdate()

    current_month = today.month
    current_year = today.year

    total_properties = Renting.objects.count()

    paid = MonthlyRent.objects.filter(
        paid=True,
        month=current_month,
        year=current_year
    ).count()

    unpaid = MonthlyRent.objects.filter(
        paid=False,
        month=current_month,
        year=current_year
    ).count()

    vacant = Renting.objects.filter(
        Q(temp_owner__isnull=True) |
        Q(temp_owner="") |
        Q(temp_owner=" ")
    ).count()

    expiring = Renting.objects.filter(
        property_expiry_date__isnull=False
    ).count()

    total_amount_this_month = Renting.objects.aggregate(
        total=Sum("rent_income")
    )["total"] or 0

    return Response({
        "total_properties": total_properties,
        "paid": paid,
        "unpaid": unpaid,
        "vacant": vacant,
        "expiring": expiring,
        "total_amount_this_month": total_amount_this_month,
    })


@api_view(["GET"])
def search_tenant(request):

    query = request.GET.get("q", "")

    tenants = Renting.objects.filter(
        Q(property_id__icontains=query) |
        Q(temp_owner__icontains=query) |
        Q(mob_number__icontains=query)
    ).order_by("property_id")

    serializer = RentingSerializer(tenants, many=True)

    return Response(serializer.data)
 
@api_view(["POST"])
def add_property(request):
 
    serializer = RentingSerializer(data=request.data)
 
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Property Added Successfully",
                "property": serializer.data,
            },
            status=201,
        )
 
    return Response(
        {
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors,
        },
        status=400,
    )

@api_view(["PUT"])
def pay_rent(request, property_id, year, month):

    rent = get_object_or_404(
    MonthlyRent,
    property__property_id=property_id,
    year=year,
    month=month,
    )

    rent.paid = True
    rent.payment_date = timezone.now().date()
    rent.save()

    return Response({
        "status": "success",
        "message": "Rent Paid Successfully"
    })


@api_view(["PUT"])
def undo_rent(request, property_id, year, month):

    rent = get_object_or_404(
    MonthlyRent,
    property__property_id=property_id,
    year=year,
    month=month,
)

    rent.paid = False
    rent.payment_date = None
    rent.save()

    return Response({
        "status": "success",
        "message": "Rent Payment Undone Successfully"
    })


@api_view(["PUT"])
def update_property(request, property_id):

    property_obj = get_object_or_404(
        Renting,
        property_id=property_id
    )

    data = request.data

    property_obj.temp_owner = data.get("temp_owner", property_obj.temp_owner)
    property_obj.mob_number = data.get("mob_number", property_obj.mob_number)
    property_obj.rent_income = data.get("rent_income", property_obj.rent_income)
    property_obj.deposit = data.get("deposit", property_obj.deposit)
    property_obj.property_address = data.get("property_address", property_obj.property_address)
    property_obj.property_type = data.get("property_type", property_obj.property_type)
    property_obj.property_issue_date = data.get("property_issue_date", property_obj.property_issue_date)
    property_obj.property_expiry_date = data.get("property_expiry_date", property_obj.property_expiry_date)

    property_obj.save()

    return Response({
        "status": "success",
        "message": "Property Updated Successfully"
    })


from django.db.models import Q

@api_view(["GET"])
def electricity_list(request):
    year = request.GET.get("year")
    month = request.GET.get("month")

    bills = (
        ElectricityBills.objects
        .select_related("property")
        .exclude(property__temp_owner="")
        .exclude(property__temp_owner__isnull=True)
    )

    if year:
        bills = bills.filter(year=year)
    if month:
        bills = bills.filter(month=month)

    bills = bills.order_by("property__property_id")

    serializer = ElectricityBillsSerializer(bills, many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def update_electricity(request, property_id, year, month):

    bill = get_object_or_404(
        ElectricityBills,
        property__property_id=property_id,
        year=year,
        month=month
    )

    data = request.data

    try:
        previous = float(
            data.get(
                "previous_reading",
                bill.previous_reading
            )
        )

        current = float(
            data.get(
                "current_reading",
                bill.current_reading
            )
        )

        rate = float(
            data.get(
                "rate_per_unit",
                bill.rate_per_unit or 0
            )
        )

    except (TypeError, ValueError):
        return Response(
            {
                "status": "error",
                "message": "Invalid reading or rate."
            },
            status=400,
        )

    # Always calculate positive units
    units = abs(current - previous)

    amount = units * rate

    bill.previous_reading = previous
    bill.current_reading = current
    bill.units_consumed = units
    bill.rate_per_unit = rate
    bill.total_amount = amount
    bill.remarks = data.get(
        "remarks",
        bill.remarks,
    )

    bill.save()

    serializer = ElectricityBillsSerializer(bill)

    return Response({
        "status": "success",
        "message": "Electricity updated successfully.",
        "units": units,
        "amount": amount,
        "bill": serializer.data,
    })

@api_view(["PUT"])
def pay_electricity(request, property_id, year, month):
    bill = get_object_or_404(
        ElectricityBills,
        property__property_id=property_id,
        year=year,
        month=month
    )

    bill.paid = True
    bill.payment_date = timezone.now().date()
    bill.save()

    serializer = ElectricityBillsSerializer(bill)
    return Response({
        "status": "success",
        "message": "Electricity Bill Paid",
        "bill": serializer.data
    })


@api_view(["PUT"])
def undo_electricity(request, property_id, year, month):
    bill = get_object_or_404(
        ElectricityBills,
        property__property_id=property_id,
        year=year,
        month=month
    )

    bill.paid = False
    bill.payment_date = None
    bill.save()

    serializer = ElectricityBillsSerializer(bill)
    return Response({
        "status": "success",
        "message": "Payment Undo Successfully",
        "bill": serializer.data
    })


@api_view(["GET"])
def old_tenants_all(request):

    tenants = OldTenants.objects.all().order_by("-exit_date")

    serializer = OldTenantsSerializer(
        tenants,
        many=True,
    )

    return Response(serializer.data)

@api_view(["GET"])
def rent_list(request):

    year = request.GET.get("year")
    month = request.GET.get("month")

    rents = MonthlyRent.objects.select_related("property")

    if year:
        rents = rents.filter(year=year)

    if month:
        rents = rents.filter(month=month)

    serializer = MonthlyRentSerializer(rents, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def property_all(request):

    properties = Renting.objects.all().order_by("property_id")

    serializer = RentingSerializer(
        properties,
        many=True,
    )

    return Response(serializer.data)