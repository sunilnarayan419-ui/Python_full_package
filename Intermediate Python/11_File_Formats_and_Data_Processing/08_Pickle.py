from __future__ import annotations

import logging
import pickle
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


class UntrustedPickleError(RuntimeError):
    """Raised when an attempt is made to unpickle data from a non-trusted origin."""


# SECURITY WARNING
# -----------------------------------------------------------------------
# Never unpickle data from an untrusted source. The pickle protocol can
# execute arbitrary code during deserialization (via __reduce__ and
# similar object hooks). pickle.load()/pickle.loads() must only ever be
# used on data that this same trusted system produced and controlled the
# full lifecycle of (e.g. an internal cache file written by this process).
#
# For any cross-language interchange, or for data received from another
# service, a user upload, or the network, use a non-executable format
# instead: JSON, Parquet, or HDF5 depending on the data shape.
# -----------------------------------------------------------------------

PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL


@dataclass(frozen=True, slots=True)
class TrainedModelArtifact:
    """A trusted, internally produced Python object graph.

    Represents something like a fitted scikit-learn-style model bundle:
    an object graph that is impractical to represent as JSON but is only
    ever passed between trusted processes owned by this system.
    """

    model_name: str
    feature_names: tuple[str, ...]
    coefficients: tuple[float, ...]
    training_run_id: str


def dump_artifact(artifact: TrainedModelArtifact, output_path: Path) -> None:
    """Serialize a trusted internal object with an atomic temp-file replacement."""
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with tmp_path.open("wb") as handle:
            pickle.dump(artifact, handle, protocol=PICKLE_PROTOCOL)
        tmp_path.replace(output_path)
        logger.info(
            "wrote pickle artifact '%s' (protocol=%d) to %s",
            artifact.model_name,
            PICKLE_PROTOCOL,
            output_path,
        )
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def load_trusted_artifact(input_path: Path, *, source_is_trusted: bool) -> TrainedModelArtifact:
    """Deserialize a pickle file that this system itself produced.

    The `source_is_trusted` flag must be explicitly and deliberately set
    to True by the caller; it exists so that unpickling can never happen
    accidentally on a path derived from external input.
    """
    if not source_is_trusted:
        raise UntrustedPickleError(
            "Refusing to unpickle: source_is_trusted was not explicitly set. "
            "Never unpickle data from an untrusted source."
        )

    if not input_path.is_file():
        raise FileProcessingError(f"Pickle file not found: {input_path}")

    try:
        with input_path.open("rb") as handle:
            obj = pickle.load(handle)  # noqa: S301 -- trusted, internal source only
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError) as exc:
        raise DataFormatError(f"{input_path}: could not unpickle object ({exc})") from exc

    if not isinstance(obj, TrainedModelArtifact):
        raise DataFormatError(
            f"{input_path}: unpickled object is not a TrainedModelArtifact "
            f"(got {type(obj)!r})"
        )

    logger.info("loaded trusted pickle artifact '%s' from %s", obj.model_name, input_path)
    return obj


def roundtrip_in_memory(artifact: TrainedModelArtifact) -> TrainedModelArtifact:
    """Demonstrate dumps()/loads() for trusted in-process transfer only."""
    payload = pickle.dumps(artifact, protocol=PICKLE_PROTOCOL)
    logger.info("serialized artifact to %d byte(s) in memory", len(payload))
    restored = pickle.loads(payload)  # noqa: S301 -- same-process, trusted origin
    return restored


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    artifact = TrainedModelArtifact(
        model_name="expression-classifier-v3",
        feature_names=("gene_a_expr", "gene_b_expr", "gene_c_expr"),
        coefficients=(0.42, -1.18, 0.07),
        training_run_id="RUN-2025-014",
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        pickle_path = Path(tmp_dir) / "model_artifact.pkl"
        dump_artifact(artifact, pickle_path)

        # source_is_trusted=True is valid here only because this exact
        # process wrote the file moments ago; it is not general-purpose
        # permission to unpickle files from elsewhere.
        loaded = load_trusted_artifact(pickle_path, source_is_trusted=True)
        logger.info("loaded artifact: %s", loaded.model_name)

        restored = roundtrip_in_memory(artifact)
        logger.info("in-memory roundtrip artifact: %s", restored.model_name)

        try:
            load_trusted_artifact(pickle_path, source_is_trusted=False)
        except UntrustedPickleError as exc:
            logger.warning("expected refusal for untrusted load: %s", exc)


if __name__ == "__main__":
    _demo()
