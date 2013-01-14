po2json
=======

Converts gettext .po files to javascript objects.


Usage
=======
You use the po2json command to generate all your script files:

First argument is locale path, Second is output path, and third is 
the translation domain.

    $ po2json eventray/locale/ eventray/static/translations/ eventray

Then include babel.js and all your translation files in your website.

Then toi use the translation just pass the locale name to babel:

    translations = babel.Translations.load(window["es"]).install();
    trans_text = translations.gettext(text);
