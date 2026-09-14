"""Minimal JSON-first Bootdisk catalog reference implementation.

This package intentionally uses only the Python standard library. It exists to
prove the catalog identity and reference model before choosing persistence,
framework or API technology.
"""

from .catalog import Catalog, CatalogError, CatalogValidationError

__all__ = ["Catalog", "CatalogError", "CatalogValidationError"]
