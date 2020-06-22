import datetime as dt

from django.utils.translation import gettext as _
from django.apps import apps as django_apps
from online_payments.billing.szamlazzhu.exceptions import SzamlazzhuError
from rest_framework.exceptions import ValidationError
from appointments.models import QRCode
from appointments import email

MISSING = object()

# submitted_data can be one of:
# - serializer.validated_data (staff_api)
# - form.cleaned_data (PaymentInline admin)
def validate_paid_at(original_paid_at, submitted_data: dict):
    new_paid_at = submitted_data.get("paid_at", MISSING)
    if new_paid_at is MISSING:
        return

    if original_paid_at and new_paid_at != original_paid_at:
        raise ValueError(_("Paid at can not be changed"))


def handle_paid_at(original_paid_at, seat, submitted_data: dict):
    try:
        validate_paid_at(original_paid_at, submitted_data)
    except ValueError:
        return

    if original_paid_at is None and submitted_data.get("paid_at"):
        billing = django_apps.get_app_config("billing")
        billing.service.send_seat_invoice(seat)


def complete_transaction(transaction, finish_date):
    """
    This happens in the context of simplepay payment for the entire appointment.
    """

    transaction.status = transaction.STATUS_COMPLETED
    transaction.save()

    # any payment and seat are ok to find the right appointment
    appointment = transaction.payments.first().seat.appointment
    appointment.is_registration_completed = True
    appointment.save()

    transaction.payments.all().update(paid_at=finish_date)

    for seat in appointment.seats.all():
        QRCode.objects.create(seat=seat)

    # Need to query seats again
    for seat in appointment.seats.all():
        if not seat.email:
            raise ValidationError({"email": "Email field is required"})
        email.send_qrcode(seat)

    try:
        billing = django_apps.get_app_config("billing")
        billing.service.send_appointment_invoice(appointment)
    except SzamlazzhuError as e:
        raise ValidationError({"error": str(e)})
