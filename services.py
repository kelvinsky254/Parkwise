from .models import PaymentSession


def initiate_payment_session(
        user,
        lot: ParkingLot,
        vehicle: Vehicle,
        latitude: float = None,
        longitude: float = None,
) -> PaymentSession:
    """
    Core orchestration:
    1. Resolve the active vendor for this parking lot
    2. Build the USSD payload through the vendor adapter
    3. Persist a PaymentSession for audit
    4. Return the session (caller renders ussd_string + tel_uri)
    """
    vendor = _get_active_vendor(lot)
    if not vendor:
        raise ValueError(f"No active vendor for lot '{lot.name}'")

    payload = build_ussd_payload(
        vendor=vendor,
        plate=vehicle.plate_number,
        phone=user.phone_number,
        lot_name=lot.name,
    )

    session = PaymentSession.objects.create(
        user=user,
        vehicle=vehicle,
        lot=lot,
        vendor=vendor,
        plate_number=payload.plate_number,
        phone_number=payload.phone_number,
        ussd_string=payload.ussd_string,
        tel_uri=payload.tel_uri,
        user_latitude=latitude,
        user_longitude=longitude,
    )
    return session