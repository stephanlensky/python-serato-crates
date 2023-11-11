import struct
from pathlib import Path
from typing import Any


def _decode_struct(data):
    ret = []
    i = 0
    while i < len(data):
        tag = data[i : i + 4].decode("ascii")
        length = struct.unpack(">I", data[i + 4 : i + 8])[0]
        value = data[i + 8 : i + 8 + length]
        value = _decode(value, tag=tag)
        ret.append((tag, value))
        i += 8 + length
    return ret


def _decode_unicode(data):
    return data.decode("utf-16-be")


def _decode_unsigned(data):
    return struct.unpack(">I", data)[0]


def _noop(data):
    return data


def _decode(data, tag=None):
    decode_func_full = {
        None: _decode_struct,
        "vrsn": _decode_unicode,
        "sbav": _noop,
    }

    decode_func_first = {
        "o": _decode_struct,
        "t": _decode_unicode,
        "p": _decode_unicode,
        "u": _decode_unsigned,
        "b": _noop,
    }

    if tag in decode_func_full:
        decode_func = decode_func_full[tag]
    else:
        decode_func = decode_func_first[tag[0]]

    return decode_func(data)


def _encode_struct(data):
    ret = b""
    for tag, value in data:
        ret += tag.encode("ascii")
        encoded_value = _encode(value, tag=tag)
        ret += struct.pack(">I", len(encoded_value))
        ret += encoded_value
    return ret


def _encode_unicode(data):
    return data.encode("utf-16-be")


def _encode_unsigned(data):
    return struct.pack(">I", data)


def _noop(data):
    return data


def _encode(data, tag=None):
    encode_func_full = {
        None: _encode_struct,
        "vrsn": _encode_unicode,
        "sbav": _noop,
    }

    encode_func_first = {
        "o": _encode_struct,
        "t": _encode_unicode,
        "p": _encode_unicode,
        "u": _encode_unsigned,
        "b": _noop,
    }

    if tag in encode_func_full:
        encode_func = encode_func_full[tag]
    else:
        encode_func = encode_func_first[tag[0]]

    return encode_func(data)


def read_crate_file(path: Path) -> list[tuple[str, Any]]:
    with open(path, "rb") as f:
        decoded = _decode(f.read())

    return decoded


def write_crate_file(path: Path, data: list[tuple[str, Any]]) -> None:
    with open(path, "wb") as f:
        f.write(_encode(data))
