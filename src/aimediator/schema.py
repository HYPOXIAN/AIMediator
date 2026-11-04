"""JSON-schema builders and constants for model response formats."""


def obj(properties):
    return {'type': 'object', 'additionalProperties': False,
            'properties': properties, 'required': list(properties)}


def arr(items):
    return {'type': 'array', 'items': items}


STRING = {'type': 'string', 'minLength': 1}
NULL_STRING = {'type': ['string', 'null']}
BOOL = {'type': 'boolean'}
