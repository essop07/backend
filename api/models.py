from django.db import models


class Renting(models.Model):
    property_id = models.TextField(unique=True)
    panchayat_id = models.TextField(unique=True, blank=True, null=True)
    nagarpalika_id = models.TextField(unique=True, blank=True, null=True)
    temp_owner = models.TextField(blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    mob_number = models.TextField(blank=True, null=True)
    rent_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    property_issue_date = models.TextField(blank=True, null=True)
    property_expiry_date = models.TextField(blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    property_type = models.TextField(blank=True, null=True)
    on_paper = models.TextField(blank=True, null=True)
    real_owner = models.TextField(blank=True, null=True)
    agreement_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "renting"


class MonthlyRent(models.Model):
    property = models.ForeignKey(
        Renting,
        models.DO_NOTHING,
        to_field="property_id",
        db_column="property_id",
        blank=True,
        null=True,
    )
    year = models.IntegerField()
    month = models.IntegerField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "monthly_rent"


class OldTenants(models.Model):
    property_id = models.CharField(max_length=50)
    old_tenant_name = models.TextField()
    old_mobile = models.TextField(blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    exit_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "old_tenants"


class ElectricityBills(models.Model):
    property = models.ForeignKey(
        Renting,
        models.DO_NOTHING,
        to_field="property_id",
        db_column="property_id",
    )
    year = models.IntegerField()
    month = models.IntegerField()
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    units_consumed = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "electricity_bills"
        unique_together = (("property", "year", "month"),)

