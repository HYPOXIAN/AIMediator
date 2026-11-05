"""Versioned configuration with explicit credentials and no global discovery."""
import math
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from .common import Failure, read
from .resources import asset_path


def defaults():
    return {'schema_version': 'aimediator-config-v1',
            'base_url': 'http://127.0.0.1:11434',
            'routing': read(asset_path('configs/local-language-routing.json')),
            'inference_options': {'temperature': 0, 'seed': 42, 'num_ctx': 8192},
            'connection_timeout': 10, 'request_timeout': 1800,
            'embedding': {'provider': 'ollama', 'model': 'qwen3-embedding:8b',
                          'endpoint': None, 'credential_env': 'EMBEDDING_API_KEY'},
            'evidence_quality': 'off', 'stop_after': 'full', 'num_gpu': None,
            'max_parallel_requests': 1, 'cache_dir': None,
            'report_scope': 'collection_sample'}


def endpoint(value):
    if not isinstance(value, str):
        raise Failure(2, 'Endpoint must be an HTTP(S) URL')
    p = urlsplit(value)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise Failure(2, 'Endpoint must be HTTP(S), without credentials, query or fragment')
    return value.rstrip('/')


def embedding_endpoint(value: str) -> str:
    parsed = urlsplit(endpoint(value))
    path = parsed.path.rstrip('/')
    if path.endswith('/chat/completions'):
        path = path[:-len('/chat/completions')] + '/embeddings'
    elif not path.endswith('/embeddings'):
        path += '/embeddings'
    return urlunsplit((parsed.scheme, parsed.netloc, path, '', ''))


def env_values(path=None):
    values = {}
    if path:
        for line in Path(path).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.removeprefix('export ').split('=', 1)
            value = value.strip()
            if value[:1] in ('"', "'") and value[-1:] == value[:1]:
                value = value[1:-1]
            values[key.strip()] = value
    return values


def credential(cfg, env_file=None, required=True):
    if cfg['embedding']['provider'] != 'configured':
        return None
    name = cfg['embedding']['credential_env']
    value = os.environ.get(name) or env_values(env_file).get(name)
    if not value and required:
        raise Failure(3, 'Configured embedding credential unavailable: ' + name)
    return value


def validate(cfg):
    d = defaults()
    if set(cfg) != set(d) or cfg['schema_version'] != d['schema_version']:
        raise Failure(2, 'Unknown or missing configuration keys/schema')
    if not isinstance(cfg['embedding'], dict) or set(cfg['embedding']) != set(d['embedding']):
        raise Failure(2, 'Unknown or missing embedding configuration keys')
    e = cfg['embedding']
    endpoint(cfg['base_url'])
    if e['provider'] not in ('ollama', 'configured') or not isinstance(e['model'], str) or not e['model'].strip():
        raise Failure(2, 'Invalid embedding provider/model')
    if not isinstance(e['credential_env'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', e['credential_env']):
        raise Failure(2, 'Invalid credential environment-variable name')
    if e['endpoint'] is not None:
        endpoint(e['endpoint'])
        if e['provider'] == 'configured':
            e['endpoint'] = embedding_endpoint(e['endpoint'])
    if e['provider'] == 'configured' and not e['endpoint']:
        raise Failure(2, 'Configured embedding requires an explicit endpoint')
    if cfg['routing'] != d['routing']:
        raise Failure(2, 'V1 preserves the packaged bilingual model/prompt routing')
    if cfg['inference_options'] != d['inference_options']:
        raise Failure(2, 'V1 preserves the existing inference options')
    for key in ('connection_timeout', 'request_timeout'):
        if type(cfg[key]) not in (int, float) or not math.isfinite(cfg[key]) or not 0 < cfg[key] <= 3600:
            raise Failure(2, 'Timeouts must be finite, positive and at most 3600 seconds')
    if cfg['num_gpu'] is not None and (type(cfg['num_gpu']) is not int or cfg['num_gpu'] < 0):
        raise Failure(2, 'num_gpu must be a nonnegative integer or null')
    if type(cfg['max_parallel_requests']) is not int or not 1 <= cfg['max_parallel_requests'] <= 8:
        raise Failure(2, 'max_parallel_requests must be an integer from 1 to 8')
    if cfg['cache_dir'] is not None and (not isinstance(cfg['cache_dir'], str) or not cfg['cache_dir'].strip()):
        raise Failure(2, 'cache_dir must be a nonempty path or null')
    if cfg['report_scope'] != 'collection_sample':
        raise Failure(2, 'Only collection_sample report scope is supported')
    if cfg['evidence_quality'] not in ('off', 'shadow', 'enforce') or cfg['stop_after'] not in ('relevance', 'quality', 'full'):
        raise Failure(2, 'Invalid quality mode or stop stage')
    if cfg['stop_after'] == 'relevance' and cfg['evidence_quality'] != 'off':
        raise Failure(2, 'Stopping after relevance requires quality=off')
    if cfg['stop_after'] == 'quality' and cfg['evidence_quality'] == 'off':
        raise Failure(2, 'Stopping after quality requires shadow/enforce')
    return cfg


def resolve(path=None, overrides=None, env_file=None):
    cfg = defaults()
    if path:
        supplied = read(path)
        if not isinstance(supplied, dict) or set(supplied) - set(cfg):
            raise Failure(2, 'Unknown configuration keys')
        cfg.update(supplied)
        # A relative cache directory in a configuration file resolves against that file.
        if isinstance(cfg['cache_dir'], str) and cfg['cache_dir'].strip():
            cfg['cache_dir'] = str((Path(path).resolve().parent / cfg['cache_dir']).resolve())
    # A supplied env file may configure an explicit configured provider; it is never discovered.
    overrides = overrides or {}
    for key, value in overrides.items():
        if value is None:
            continue
        if key.startswith('embedding_'):
            cfg['embedding'][key[len('embedding_'):]] = value
        elif key == 'cache_dir':
            # A CLI path resolves from the invocation directory.
            cfg[key] = str(Path(value).resolve())
        else:
            cfg[key] = value
    if cfg['embedding']['provider'] == 'configured':
        values = env_values(env_file)
        if not cfg['embedding']['endpoint']:
            cfg['embedding']['endpoint'] = os.environ.get('EMBEDDING_API_URL') or values.get('EMBEDDING_API_URL')
        if not overrides.get('embedding_model') and not path:
            cfg['embedding']['model'] = os.environ.get('EMBEDDING_MODEL') or values.get('EMBEDDING_MODEL') or cfg['embedding']['model']
    return validate(cfg)
