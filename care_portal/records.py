"""Non-diagnostic, demo-only result availability and follow-up records."""

from __future__ import annotations

from dataclasses import asdict, dataclass


class AccessDeniedError(ValueError):
    """Raised without disclosing whether a patient record exists."""


@dataclass(frozen=True)
class PortalRecord:
    id: str
    category: str
    title: str
    published_at: str
    availability: str
    staff_follow_up: bool
    follow_up_message: str


DEMO_ACCESS_CODE = "DEMO-4821"
_DEMO_RECORDS = (
    PortalRecord("result-01", "Resultado", "Informe de laboratorio", "06 oct 2026", "Disponible", True,
                 "El equipo de la clínica solicitó una revisión administrativa de seguimiento. Comunícate con recepción."),
    PortalRecord("order-02", "Orden", "Orden de control", "04 oct 2026", "Disponible", False,
                 "No hay acciones administrativas pendientes."),
    PortalRecord("prescription-03", "Receta", "Receta electrónica", "01 oct 2026", "Disponible", False,
                 "No hay acciones administrativas pendientes."),
)


def portal_payload(access_code: str) -> dict:
    """Return generic demo resources; never contains patient identity or clinical values."""
    _validate_access_code(access_code)
    return {
        "demo": True,
        "notice": "Demo: estos son datos de ejemplo, no resultados médicos reales.",
        "records": [asdict(record) for record in _DEMO_RECORDS],
    }


def acknowledge_follow_up(access_code: str, record_id: str) -> dict:
    _validate_access_code(access_code)
    if record_id not in {record.id for record in _DEMO_RECORDS}:
        raise ValueError("No fue posible completar la solicitud.")
    return {"success": True, "message": "Tu solicitud fue registrada para seguimiento por recepción."}


def _validate_access_code(access_code: str) -> None:
    if access_code.strip().upper() != DEMO_ACCESS_CODE:
        raise AccessDeniedError("No fue posible acceder al portal. Revisa tu código o contacta a recepción.")
