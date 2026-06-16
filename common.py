import importlib
import os
import statistics


PARAMS = [
    ("SLH-DSA-SHA2-128s", "pyspx.sha2_128s"),
    ("SLH-DSA-SHA2-128f", "pyspx.sha2_128f"),
    ("SLH-DSA-SHA2-192s", "pyspx.sha2_192s"),
    ("SLH-DSA-SHA2-192f", "pyspx.sha2_192f"),
    ("SLH-DSA-SHA2-256s", "pyspx.sha2_256s"),
    ("SLH-DSA-SHA2-256f", "pyspx.sha2_256f"),
]


def load_module(module_name):
    return importlib.import_module(module_name)


def generate_keypair(spx):
    seed = os.urandom(spx.crypto_sign_SEEDBYTES)
    return spx.generate_keypair(seed)


def safe_verify(spx, message, signature, public_key):
    try:
        return bool(spx.verify(message, signature, public_key))
    except Exception:
        return False


def mean_ms(values_ns):
    return statistics.mean(values_ns) / 1_000_000


def std_ms(values_ns):
    if len(values_ns) <= 1:
        return 0.0
    return statistics.stdev(values_ns) / 1_000_000
