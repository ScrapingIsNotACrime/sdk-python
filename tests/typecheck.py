"""Validates a JSON value against a TypedDict-based type at runtime (tests only)."""

from __future__ import annotations

import types
import typing
from typing import (
    Any,
    Literal,
    NotRequired,
    Required,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)


def _strip(hint: Any) -> Any:
    while get_origin(hint) in (NotRequired, Required):
        hint = get_args(hint)[0]
    return hint


def check(value: Any, hint: Any, path: str = "$") -> list[str]:
    hint = _strip(hint)
    if hint is Any:
        return []
    origin = get_origin(hint)
    if origin in (Union, types.UnionType):
        errors = [check(value, arg, path) for arg in get_args(hint)]
        return [] if any(not e for e in errors) else [f"{path}: {value!r:.60} matches no member of {hint}"]
    if origin is Literal:
        return [] if value in get_args(hint) else [f"{path}: {value!r} not in {get_args(hint)}"]
    if origin is list:
        if not isinstance(value, list):
            return [f"{path}: expected list, got {type(value).__name__}"]
        (item,) = get_args(hint)
        return [error for i, element in enumerate(value) for error in check(element, item, f"{path}[{i}]")]
    if origin is dict:
        return [] if isinstance(value, dict) else [f"{path}: expected object"]
    if is_typeddict(hint):
        if not isinstance(value, dict):
            return [f"{path}: expected object, got {type(value).__name__}"]
        hints = get_type_hints(hint, include_extras=True)
        field_errors = [f"{path}.{key}: missing" for key in hint.__required_keys__ if key not in value]
        for key, element in value.items():
            if key in hints:
                field_errors.extend(check(element, hints[key], f"{path}.{key}"))
        return field_errors
    if hint is type(None):
        return [] if value is None else [f"{path}: expected null, got {value!r:.60}"]
    if hint is bool:
        return [] if isinstance(value, bool) else [f"{path}: expected bool, got {value!r:.60}"]
    if hint is int:
        ok = isinstance(value, int) and not isinstance(value, bool)
        return [] if ok else [f"{path}: expected int, got {value!r:.60}"]
    if hint is float:
        ok = isinstance(value, int | float) and not isinstance(value, bool)
        return [] if ok else [f"{path}: expected number, got {value!r:.60}"]
    if hint is str:
        return [] if isinstance(value, str) else [f"{path}: expected str, got {value!r:.60}"]
    raise TypeError(f"unsupported hint at {path}: {hint!r}")


__all__ = ["check", "typing"]
