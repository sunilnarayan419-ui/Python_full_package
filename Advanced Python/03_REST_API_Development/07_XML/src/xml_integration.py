from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from xml.etree.ElementTree import Element, ParseError, SubElement, tostring

from defusedxml.ElementTree import fromstring

_ASSAY_NAMESPACE = "urn:research-platform:assay-results:v1"
_NAMESPACE_MAP = {"assay": _ASSAY_NAMESPACE}


@dataclass(slots=True)
class AssayResult:
    compound_id: str
    target_protein: str
    measured_value: float
    unit: str
    measured_at: datetime


class XmlIntegrationError(Exception):
    pass


def assay_result_to_xml(result: AssayResult) -> bytes:
    root = Element(f"{{{_ASSAY_NAMESPACE}}}AssayResult")
    root.set("compoundId", result.compound_id)

    target = SubElement(root, f"{{{_ASSAY_NAMESPACE}}}TargetProtein")
    target.text = result.target_protein

    measurement = SubElement(root, f"{{{_ASSAY_NAMESPACE}}}Measurement")
    measurement.set("unit", result.unit)
    measurement.text = f"{result.measured_value:.4f}"

    timestamp = SubElement(root, f"{{{_ASSAY_NAMESPACE}}}MeasuredAt")
    timestamp.text = result.measured_at.isoformat()

    return tostring(root, encoding="utf-8", xml_declaration=True)


def xml_to_assay_result(raw_xml: bytes) -> AssayResult:
    try:
        root = fromstring(raw_xml, forbid_dtd=True, forbid_entities=True, forbid_external=True)
    except ParseError as exc:
        raise XmlIntegrationError(f"Malformed assay result XML: {exc}") from exc

    compound_id = root.get("compoundId")
    if not compound_id:
        raise XmlIntegrationError("Missing required 'compoundId' attribute on AssayResult root element.")

    target_element = root.find(f"{{{_ASSAY_NAMESPACE}}}TargetProtein")
    measurement_element = root.find(f"{{{_ASSAY_NAMESPACE}}}Measurement")
    timestamp_element = root.find(f"{{{_ASSAY_NAMESPACE}}}MeasuredAt")

    if target_element is None or measurement_element is None or timestamp_element is None:
        raise XmlIntegrationError("Assay result XML is missing one or more required elements.")

    unit = measurement_element.get("unit")
    if not unit:
        raise XmlIntegrationError("Measurement element is missing the required 'unit' attribute.")

    try:
        measured_value = float(measurement_element.text or "")
        measured_at = datetime.fromisoformat(timestamp_element.text or "")
    except ValueError as exc:
        raise XmlIntegrationError(f"Invalid numeric or timestamp value in assay result XML: {exc}") from exc

    return AssayResult(
        compound_id=compound_id,
        target_protein=target_element.text or "",
        measured_value=measured_value,
        unit=unit,
        measured_at=measured_at,
    )
