import os
import random
import string

import collections
import requests


def file_upload(path: str, url: str, fields: dict, header: dict) -> str:
    files = {
        "file": open(path, "rb")
    }
    response = requests.request("POST", url=url, data=fields, files=files, headers=header)
    return str(response.content, encoding='utf-8')


def _namedtuple(typename, fields, default_values=()):
    T = collections.namedtuple(typename, fields)
    T.__new__.__defaults__ = (None,) * len(fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T


File = _namedtuple('File', ['filename', 'fieldname', 'mimetype'])


def _multipart(fileds: dict, file: File):
    boundary = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(30))
    special_separator = "--" + boundary
    lines = []

    # fileds
    for name, value in fileds.items():
        lines.extend((
            special_separator,
            'Content-Disposition: form-data; name="%s"' % str(name),
            '',
            str(value.encode("utf-8")),
        ))

    # file
    _, filename = os.path.split(file.filename)
    with open(file.filename, 'rb', buffering=8192, encoding='utf-8') as fd:
        lines.extend((
            special_separator,
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                str(file.fieldname), filename),
            'Content-Type: %s' % str(file.mimetype),
            '',
            str(fd.readall()),
        ))

    # end
    lines.extend((
        special_separator + "--",
        '',
    ))

    body = "\r\n".join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
        'Content-Length': str(len(body)),
    }

    return body, headers


def file_upload(path: str, url: str, fileds: dict) -> str:
    file = File(filename=path, fieldname="file", mimetype="application/octet-stream")
    data, headers = _multipart(fileds, file)

    response = requests.request("POST", url=url, headers=headers, data=data, verify=False)
    return str(response.content, encoding='utf-8')
