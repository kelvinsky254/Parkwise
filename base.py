from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.vendors.models import Vendor


@dataclass
class USSDPayload:
    """Structured result from building a USSD payment string"""
    ussd_string:str #The full chained string: *483*1*KBX123Y*0722000000#
    tel_uri:str    #tel: URI for the dialer deeplink
    display_code: str #Human-readable version shown in the UI
    lot_name: str
    plate_number: str
    phone_number: str


class BaseVendorAdapter(ABC):
    def __init__(self, vendor:"Vendor"):
        self.vendor = vendor

        @abstractmethod
        def build_ussd_payload(self, plate: str, phone: str, lot_name:str) -> USSDPayload:
            """
            Construct the USSD string for this vendor.
            plate: normalised plate number like KBX123Y
            phone: user's phone number e.g. 0722000000
            lot_name: name of the parking lot for display
            """
            ...
    def _format_chain(self, plate:str, phone:str) -> str:
        """Apply plate + phone to the vendor's USSD chain template."""
        return self.vendor.ussd_chain_template.format(plate=plate, phone=phone)

    def _to_tel_url(self, ussd_string: str) -> str:
        """Convert USSD string to a tel: deeplink the phone dialer can open."""
        encoded = ussd_string.replace("#", "%23")
        return f"tel:{encoded}"