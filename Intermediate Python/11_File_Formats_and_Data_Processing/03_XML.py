from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, SubElement

logger = logging.getLogger(__name__)

try:
    # defusedxml hardens the standard library XML parser against entity
    # expansion attacks, external entity injection, and other XML-specific
    # denial-of-service vectors. It is strongly preferred whenever XML may
    # originate from an untrusted source.
    from defusedxml.ElementTree import parse as safe_parse
    from defusedxml.ElementTree import iterparse as safe_iterparse

    _DEFUSEDXML_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on environment
    _DEFUSEDXML_AVAILABLE = False
    safe_parse = None
    safe_iterparse = None


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class DataValidationError(ValueError):
    """Raised when parsed data fails scientific validation."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


class XMLSecurityError(RuntimeError):
    """Raised when a hardened XML parser is unavailable for untrusted input."""


@dataclass(frozen=True, slots=True)
class AssayResult:
    sample_id: str
    compound: str
    concentration_um: float


def _require_defusedxml() -> None:
    if not _DEFUSEDXML_AVAILABLE:
        raise XMLSecurityError(
            "defusedxml is not installed; refusing to parse XML from an "
            "untrusted source with the standard-library parser. Install "
            "defusedxml or restrict parsing to fully trusted, internally "
            "generated XML."
        )


def _parse_assay_element(elem: Element, line_context: str) -> AssayResult:
    sample_id = elem.get("sample_id")
    compound_elem = elem.find("compound")
    concentration_elem = elem.find("concentration_um")

    if sample_id is None:
        raise DataFormatError(f"{line_context}: missing sample_id attribute")
    if compound_elem is None or compound_elem.text is None:
        raise DataFormatError(f"{line_context}: missing <compound> element")
    if concentration_elem is None or concentration_elem.text is None:
        raise DataFormatError(f"{line_context}: missing <concentration_um> element")

    try:
        concentration_um = float(concentration_elem.text)
    except ValueError as exc:
        raise DataFormatError(
            f"{line_context}: invalid concentration_um value "
            f"{concentration_elem.text!r}"
        ) from exc

    if concentration_um < 0:
        raise DataValidationError(f"{line_context}: concentration_um cannot be negative")

    return AssayResult(
        sample_id=sample_id,
        compound=compound_elem.text,
        concentration_um=concentration_um,
    )


def load_assay_results(xml_path: Path, *, trusted_source: bool = False) -> list[AssayResult]:
    """Parse a small/medium trusted-format assay-results XML document.

    For untrusted input, defusedxml is required. Set trusted_source=True
    only for XML generated internally by this same system.
    """
    if not xml_path.is_file():
        raise FileProcessingError(f"XML file not found: {xml_path}")

    if trusted_source and _DEFUSEDXML_AVAILABLE:
        tree = safe_parse(str(xml_path))
        root = tree.getroot()
    elif trusted_source:
        # Internally generated, fully trusted XML only; never use this
        # branch for XML received from an external or untrusted source.
        import xml.etree.ElementTree as ET

        root = ET.parse(xml_path).getroot()
    else:
        _require_defusedxml()
        tree = safe_parse(str(xml_path))
        root = tree.getroot()

    if root.tag != "assay_results":
        raise DataFormatError(
            f"{xml_path}: unexpected root element {root.tag!r}, "
            "expected 'assay_results'"
        )

    results: list[AssayResult] = []
    for index, result_elem in enumerate(root.findall("result")):
        context = f"{xml_path}:result[{index}]"
        results.append(_parse_assay_element(result_elem, context))

    logger.info("loaded %d assay result(s) from %s", len(results), xml_path)
    return results


def iter_assay_results_large(xml_path: Path, *, trusted_source: bool = False):
    """Iteratively parse a large assay-results XML file using iterparse.

    Elements are cleared after processing to bound memory usage regardless
    of overall document size.
    """
    if not xml_path.is_file():
        raise FileProcessingError(f"XML file not found: {xml_path}")

    if trusted_source and not _DEFUSEDXML_AVAILABLE:
        import xml.etree.ElementTree as ET

        context = ET.iterparse(str(xml_path), events=("end",))
    else:
        _require_defusedxml()
        context = safe_iterparse(str(xml_path), events=("end",))

    for index, (_event, elem) in enumerate(context):
        if elem.tag == "result":
            yield _parse_assay_element(elem, f"{xml_path}:result[{index}]")
            elem.clear()


def write_assay_results(xml_path: Path, results: list[AssayResult]) -> None:
    """Serialize assay results to XML with an atomic temp-file replacement."""
    root = Element("assay_results")
    for result in results:
        result_elem = SubElement(root, "result", {"sample_id": result.sample_id})
        compound_elem = SubElement(result_elem, "compound")
        compound_elem.text = result.compound
        concentration_elem = SubElement(result_elem, "concentration_um")
        concentration_elem.text = f"{result.concentration_um:.4f}"

    tmp_path = xml_path.with_suffix(xml_path.suffix + ".tmp")
    try:
        ElementTree(root).write(tmp_path, encoding="utf-8", xml_declaration=True)
        tmp_path.replace(xml_path)
        logger.info("wrote %d assay result(s) to %s", len(results), xml_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    results = [
        AssayResult("S-01", "Compound-A", 12.5),
        AssayResult("S-02", "Compound-B", 4.75),
        AssayResult("S-03", "Compound-A", 8.1),
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        xml_path = Path(tmp_dir) / "assay_results.xml"
        write_assay_results(xml_path, results)

        if _DEFUSEDXML_AVAILABLE:
            loaded = load_assay_results(xml_path)
            logger.info("loaded %d result(s) via hardened parser", len(loaded))

            for streamed in iter_assay_results_large(xml_path):
                logger.info("streamed result: %s", streamed.sample_id)
        else:
            logger.warning(
                "defusedxml not installed; skipping untrusted-parse demo. "
                "Install defusedxml for production use with external XML."
            )
            loaded = load_assay_results(xml_path, trusted_source=True)
            logger.info("loaded %d result(s) via trusted-source fallback", len(loaded))


if __name__ == "__main__":
    _demo()
