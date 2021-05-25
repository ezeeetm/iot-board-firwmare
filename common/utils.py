import json
import os

def test_path(fname):
    """Returns True if file at path fname exists
    otherwise, returns False."""
    try:
        with open(fname):
            pass
        return True
    except OSError:
        return False

def get_config(config_file):
    """Reads a JSON config file, adds TLS keys for MQTT,
    returns a python dict of config values."""
    with open(config_file) as f:
        config = json.load(f)
        f.close()
    fnames = os.listdir()
    config['mqtt']['cert'] = read_pem(fnames, '.crt')
    config['mqtt']['key'] = read_pem(fnames, '.key')
    return config

def read_pem(fnames, ext):
    """Reads file contents based on extension,
    used to extract text from TLS .crt and .key certificates.
    """
    for fname in filter(lambda x:x.endswith((ext)), fnames):
        with open(fname) as f:
            contents = f.read()
    return contents