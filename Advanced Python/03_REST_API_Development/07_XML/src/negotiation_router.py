from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response, status

from .xml_integration import AssayResult, XmlIntegrationError, assay_result_to_xml, xml_to_assay_result

router = APIRouter(prefix="/api/v1", tags=["assay-results"])

_STORE: dict[str, AssayResult] = {
    "CMP-0001": AssayResult(
        compound_id="CMP-0001",
        target_protein="EGFR",
        measured_value=12.45,
        unit="nM",
        measured_at=datetime.now(timezone.utc),
    )
}


@router.get("/assay-results/{compound_id}")
async def get_assay_result(
    compound_id: str,
    accept: Annotated[str, Header()] = "application/json",
) -> Response:
    result = _STORE.get(compound_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assay result not found.")

    if "application/xml" in accept:
        return Response(content=assay_result_to_xml(result), media_type="application/xml")

    payload = {
        "compound_id": result.compound_id,
        "target_protein": result.target_protein,
        "measured_value": result.measured_value,
        "unit": result.unit,
        "measured_at": result.measured_at.isoformat(),
    }
    return Response(content=str(payload).replace("'", '"'), media_type="application/json")


@router.post("/assay-results/import", status_code=status.HTTP_201_CREATED)
async def import_legacy_assay_result(
    content_type: Annotated[str, Header()],
    body: bytes,
) -> dict[str, str]:
    if "application/xml" not in content_type:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="This endpoint only accepts application/xml for legacy instrument integration.",
        )
    try:
        result = xml_to_assay_result(body)
    except XmlIntegrationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    _STORE[result.compound_id] = result
    return {"status": "imported", "compound_id": result.compound_id}
