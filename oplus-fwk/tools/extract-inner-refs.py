#!/usr/bin/env python3
#
# Copyright (C) 2026 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#
"""Extract every com.oneplus.inner.* reference from the stock 7 Pro camera dex.

The camera APKs are not checked in, so this walks baksmali output produced from
a stock dump and records exactly what the calling code needs from each wrapper:

  - every invoke-kind, so the stub knows static vs instance vs constructor
  - every field access, with the field type
  - .implements / .super, so a stub that is extended or implemented is emitted
    as a non-final class or an interface instead of a final class

The result is the model generate-stubs.py consumes. Keeping it as a separate,
checked-in tool means the stubs can be regenerated instead of hand-edited.

Usage:
    baksmali d classes.dex -o smali/          # for each dex of the three APKs
    ./extract-inner-refs.py --smali smali/ --out inner_model.json
"""

import argparse
import glob
import json
import os
import re
from collections import defaultdict

METHOD_RE = re.compile(
    r'invoke-(static|virtual|interface|direct|super)(?:/range)?\s*\{[^}]*\},\s*'
    r'Lcom/oneplus/inner/([A-Za-z0-9_/$]+);->([A-Za-z0-9_$<>]+)(\([^)]*\)[^ \n#]+)')

FIELD_RE = re.compile(
    r'\b(iget|iput|sget|sput)(?:-[a-z]+)?\s+[vp]\d+(?:,\s*[vp]\d+)?,\s*'
    r'Lcom/oneplus/inner/([A-Za-z0-9_/$]+);->([A-Za-z0-9_$]+):([^ \n#]+)')

TYPE_RE = re.compile(r'Lcom/oneplus/inner/([A-Za-z0-9_/$]+);')
IMPLEMENTS_RE = re.compile(r'^\.implements Lcom/oneplus/inner/([A-Za-z0-9_/$]+);',
                           re.M)
SUPER_RE = re.compile(r'^\.super Lcom/oneplus/inner/([A-Za-z0-9_/$]+);', re.M)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smali', required=True,
                        help='baksmali output root (searched recursively)')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    methods = defaultdict(set)
    fields = defaultdict(set)
    kinds = defaultdict(dict)
    interfaces = set()
    supers = set()
    all_types = set()

    for path in glob.glob(os.path.join(args.smali, '**', '*.smali'),
                          recursive=True):
        with open(path, errors='replace') as handle:
            text = handle.read()
        if 'Lcom/oneplus/inner/' not in text:
            continue

        all_types.update(TYPE_RE.findall(text))
        interfaces.update(IMPLEMENTS_RE.findall(text))
        supers.update(SUPER_RE.findall(text))

        for op, cls, name, sig in METHOD_RE.findall(text):
            kind = ('static' if op == 'static'
                    else 'constructor' if name == '<init>' else 'instance')
            methods[cls].add((name, sig))
            # A method reached through more than one invoke kind is treated as
            # static only when every caller uses invoke-static; static and
            # instance cannot both be true, and the caller that uses
            # invoke-static decides.
            prior = kinds[cls].get((name, sig))
            kinds[cls][(name, sig)] = (
                'static' if 'static' in (prior, kind) else (prior or kind))

        for op, cls, name, ftype in FIELD_RE.findall(text):
            fields[cls].add((name, ftype))
            kinds[cls][('#', name, ftype)] = (
                'static' if op.startswith('s') else 'instance')

    model = {
        'methods': {c: [[n, s] for n, s in sorted(v)]
                    for c, v in methods.items()},
        'fields': {c: [[n, t] for n, t in sorted(v)]
                   for c, v in fields.items()},
        'kinds': {c: {'%s|%s' % (k[0], k[1]) if k[0] != '#'
                      else '#|%s|%s' % (k[1], k[2]): v2
                      for k, v2 in v.items()}
                  for c, v in kinds.items()},
        'interfaces': sorted(interfaces),
        'supers': sorted(supers),
        'types': sorted(all_types),
    }

    with open(args.out, 'w') as handle:
        json.dump(model, handle, indent=1, sort_keys=True)
        handle.write('\n')

    print('types=%d methods=%d fields=%d interfaces=%d supers=%d -> %s'
          % (len(all_types), len(methods), len(fields), len(interfaces),
             len(supers), args.out))


if __name__ == '__main__':
    main()
