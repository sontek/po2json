from __future__ import with_statement
from babel.messages.pofile import read_po
from simplejson import dumps

import os
import sys


def compile_to_js(po_file, lang, domain):
    print 'Compiling JavaScript for %s' % po_file

    jscatalog = {}

    with file(po_file) as f:
        catalog = read_po(f, locale=lang, domain=domain)

        for message in catalog:
            msgid = message.id
            if isinstance(msgid, (list, tuple)):
                msgid = msgid[0]
            jscatalog[msgid] = message.string

    return dumps(dict(
        messages=jscatalog,
        plural_expr=catalog.plural_expr,
        locale=str(catalog.locale),
        domain=catalog.domain
    ))


def update_js_file(po_file, lang_code, output_path, domain):
    js_content = compile_to_js(po_file, lang_code, domain)
    js_content = '%s %s %s' % (
        'window.BABEL_TO_LOAD_%s = ' % lang_code,
        js_content,
        ';'
    )

    js_file_path = os.path.join(output_path, '%s.js' % (lang_code))

    open(js_file_path, 'w').write(js_content)

def main():
    # arg 1: LOCALE path
    locale_path = sys.argv[1]
    # arg 2: Output path
    output_path = sys.argv[2]
    # arg 3: Translation Domain
    domain = sys.argv[3]

    for lang_code in os.listdir(locale_path):
        full_path = os.path.join(locale_path, lang_code)

        if os.path.isdir(full_path):
            client_po_dir = os.path.join(full_path, 'LC_MESSAGES')

            update_js_file(
                '%s/%s.po' % (client_po_dir, domain)
                , lang_code
                , output_path
                , domain
            )

if __name__ == '__main__':
    main()
