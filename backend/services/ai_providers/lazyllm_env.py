"""
Utilities for resolving LazyLLM API keys with namespace compatibility.
"""
import os


def get_lazyllm_api_key(source: str, namespace: str = "BANANA") -> str:
    """
    Resolve API key for a LazyLLM source with backward-compatible prefixes.

    Lookup order:
    1. {namespace}_{SOURCE}_API_KEY
    2. {SOURCE}_API_KEY (vendor-prefixed)
    3. BANANA_SLIDES_{SOURCE}_API_KEY (legacy docs)
    4. LAZYLLM_{SOURCE}_API_KEY (LazyLLM default)
    """
    source_upper = (source or "").upper()
    if not source_upper:
        return ""

    candidates = [
        f"{namespace}_{source_upper}_API_KEY",
        f"{source_upper}_API_KEY",
        f"BANANA_SLIDES_{source_upper}_API_KEY",
        f"LAZYLLM_{source_upper}_API_KEY",
    ]
    for key in candidates:
        value = os.getenv(key)
        if value:
            return value
    return ""


def ensure_lazyllm_namespace_key(source: str, namespace: str = "BANANA") -> bool:
    """
    Ensure LazyLLM namespace key exists by mapping legacy/default key names.
    """
    source_upper = (source or "").upper()
    if not source_upper:
        return False

    namespace_key = f"{namespace}_{source_upper}_API_KEY"
    if os.getenv(namespace_key):
        return True

    resolved_key = get_lazyllm_api_key(source, namespace=namespace)
    if resolved_key:
        os.environ[namespace_key] = resolved_key
        return True
    return False
