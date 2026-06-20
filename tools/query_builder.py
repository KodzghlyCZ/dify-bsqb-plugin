"""Shared helpers for building Brave Search queries from tool parameters."""

from __future__ import annotations

from typing import Any

from bsqb import EmptyQueryError, Query, QueryValidationError

__all__ = [
    "EmptyQueryError",
    "QueryValidationError",
    "build_query_from_parameters",
    "split_values",
]


def split_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def _as_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"false", "0", "no", "off"}:
        return False
    if text in {"true", "1", "yes", "on"}:
        return True
    return default


def build_query_from_parameters(params: dict[str, Any]) -> str:
    raw_query = str(params.get("raw_query") or "").strip()
    validate = _as_bool(params.get("validate"), default=True)

    if raw_query:
        return Query.parse(raw_query).build(validate=validate)

    main_query = str(params.get("query") or "").strip()
    if not main_query:
        raise EmptyQueryError("Provide `query` or `raw_query`.")

    query = Query(main_query)

    for phrase in split_values(params.get("phrase")):
        query = query.phrase(phrase)
    for term in split_values(params.get("include")):
        query = query.include(term)
    for term in split_values(params.get("exclude")):
        query = query.exclude(term)
    for extension in split_values(params.get("ext")):
        query = query.ext(extension)
    for filetype in split_values(params.get("filetype")):
        query = query.filetype(filetype)
    for value in split_values(params.get("intitle")):
        query = query.intitle(value)
    for value in split_values(params.get("inbody")):
        query = query.inbody(value)
    for value in split_values(params.get("inpage")):
        query = query.inpage(value)
    for code in split_values(params.get("lang")):
        query = query.lang(code)
    for code in split_values(params.get("loc")):
        query = query.loc(code)
    for domain in split_values(params.get("site")):
        query = query.site(domain)
    for fragment in split_values(params.get("raw_fragments")):
        query = query.raw(fragment)

    and_query = str(params.get("and_query") or "").strip()
    if and_query:
        query = query.and_(Query.parse(and_query))

    or_query = str(params.get("or_query") or "").strip()
    if or_query:
        query = query.or_(Query.parse(or_query))

    not_query = str(params.get("not_query") or "").strip()
    if not_query:
        query = query.not_(Query.parse(not_query))

    return query.build(validate=validate)
