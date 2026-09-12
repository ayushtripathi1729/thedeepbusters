"""Detector contracts. Implementations must never fabricate scores."""
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

@dataclass(frozen=True)
class DetectorOutput:
    manipulated_probability: float
    uncertainty: float
    evidence: dict
    model_version: str
class Detector(Protocol):
    modality: str
    def predict(self, media: Path) -> DetectorOutput: ...
class DetectorUnavailable(RuntimeError): pass
class Registry:
    def __init__(self): self._detectors = {}
    def register(self, name, detector): self._detectors[name] = detector
    def get(self, name):
        if not name or name not in self._detectors: raise DetectorUnavailable("No validated production model is registered.")
        return self._detectors[name]
registry = Registry()
