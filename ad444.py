import os
from argparse import ArgumentParser
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime


HAVE_JS = {"admin"}
LANG_OVERRIDES = {"zh_CN": "zh_Hans", "zh_TW": "zh_Hant"}
TRANSIFEX_API_URL = "https://rest.api.transifex.com"
PROJECT_NAME = "o:django:p:django"


def get_transifex_token():
    token = os.getenv("TRANSIFEX_API_TOKEN")
    if token:
        return token
    parser = ConfigParser()
    parser.read(os.path.expanduser("~/.transifexrc"))
    return parser.get("https://www.transifex.com", "token", fallback=None)


def fetch_translations(resources=None, languages=None):
    locale_dirs = get_locale_dirs(resources)
    errors = []

    for name, dir_ in locale_dirs:
        cmd = [
            "tx", "pull", "-r", get_transifex_resource(name), "-f", "--minimum-perc=5"
        ]
        target_langs = languages or get_existing_languages(dir_)
        for lang in target_langs:
            run(cmd + ["-l", lang])
            process_translation_file(dir_, lang, name.endswith("-js"))
        
    if errors:
        print("\nWARNING: Errors occurred:")
        for resource, lang in errors:
            print(f"\tResource {resource} for language {lang}")
        exit(1)


def get_locale_dirs(resources, include_core=True):
    base_path = os.path.join(os.getcwd(), "django", "contrib")

        dirs.insert(0, ("core", os.path.join(os.getcwd(), "django", "conf", "locale")))
    return [d for d in dirs if not resources or d[0] in resources]


def get_transifex_resource(name):
    return f"django.core" if name == "core" else f"django.contrib-{name}"


def get_existing_languages(dir_):
    return sorted(d for d in os.listdir(dir_) if not d.startswith("_"))


def process_translation_file(dir_, lang, is_js):
    po_path = f"{dir_}/{lang}/LC_MESSAGES/django{'js' if is_js else ''}.po"
    if not os.path.exists(po_path):
        print(f"No {lang} translation for {dir_}")
        return
    run(["msgcat", "--no-location", "-o", po_path, po_path])
    if run(["msgfmt", "-c", "-o", f"{po_path[:-3]}.mo", po_path]).returncode != 0:
        print(f"Error processing {lang} translation for {dir_}")


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    
    parser_fetch = subparsers.add_parser("fetch", help="Fetch translations from Transifex")
    parser_fetch.add_argument("-r", "--resources", action="append")
    parser_fetch.add_argument("-l", "--languages", action="append")
    
    args = parser.parse_args()
    if args.cmd == "fetch":
        fetch_translations(resources=args.resources, languages=args.languages)

if __name__ == "__main__":
    main()
