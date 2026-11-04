"""JSON-schema builders, constants and the validator for model response formats."""
from __future__ import annotations

import json
from typing import Any, Iterable


def obj(properties: dict[str, Any]) -> dict[str, Any]:
    """Object schema keyed type, additionalProperties, properties, required; the order reaches the model."""
    return {'type': 'object', 'additionalProperties': False,
            'properties': properties, 'required': list(properties)}


def quality_obj(properties: dict[str, Any]) -> dict[str, Any]:
    """Object schema keyed type, properties, required, additionalProperties; the order reaches the model."""
    return {'type': 'object', 'properties': properties, 'required': list(properties),
            'additionalProperties': False}


def arr(items: dict[str, Any]) -> dict[str, Any]:
    """Array schema with the given item schema."""
    return {'type': 'array', 'items': items}


def enum(values: Iterable[str]) -> dict[str, Any]:
    """String schema limited to the given values, in their order."""
    return {'type': 'string', 'enum': list(values)}


STRING = {'type': 'string', 'minLength': 1}
NULLABLE_STRING = {'type': ['string', 'null']}
NULLABLE_NONEMPTY_STRING = {'type': ['string', 'null'], 'minLength': 1}
BOOL = {'type': 'boolean'}


def schema_errors(value: Any, schema: dict[str, Any], path: str = '$') -> list[str]:
    """Return the errors of a value against the supported JSON-schema subset, each prefixed with its JSON path."""
    errors = []
    if 'enum' in schema and value not in schema['enum']:
        errors.append(path + ': value outside enum')
    kind = schema.get('type')
    kinds = kind if isinstance(kind, list) else [kind] if kind else []
    types = {'object': lambda v: isinstance(v, dict), 'array': lambda v: isinstance(v, list),
             'string': lambda v: isinstance(v, str), 'null': lambda v: v is None,
             'boolean': lambda v: type(v) is bool, 'integer': lambda v: type(v) is int,
             'number': lambda v: type(v) in (float, int)}
    if kinds and not any(types[k](value) for k in kinds):
        return errors + [path + ': wrong type']
    if isinstance(value, dict) and kind == 'object':
        properties = schema['properties']
        if set(schema.get('required', [])) - set(value):
            errors.append(path + ': missing keys')
        if schema.get('additionalProperties') is False and set(value) - set(properties):
            errors.append(path + ': extra keys')
        for key in set(value) & set(properties):
            errors.extend(schema_errors(value[key], properties[key], path + '.' + key))
    if isinstance(value, list) and kind == 'array':
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', float('inf')):
            errors.append(path + ': wrong item count')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(path + ': duplicate items')
        for i, item in enumerate(value):
            errors.extend(schema_errors(item, schema['items'], f'{path}[{i}]'))
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(path + ': empty string')
    if type(value) in (int, float) and not schema.get('minimum', -float('inf')) <= value <= schema.get('maximum', float('inf')):
        errors.append(path + ': outside bounds')
    return errors
