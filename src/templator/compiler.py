import glob
import os
import re
import sys

import bs4
from bs4 import BeautifulSoup

from templator.settings import ROOT_DIR

partial_infix = ".part."
pull_pattern = r"\(%\s+pull\s+([a-zA-Z_.\-\/]+)\s*%\)"


def validate_paths(input_dir: str, output_dir: str):
    input_dir_full = os.path.join(ROOT_DIR, input_dir)

    if not os.path.isdir(input_dir_full):
        raise FileNotFoundError(f'Input directory does not exist! Tried "{input_dir_full}".')

    output_dir_full = os.path.join(ROOT_DIR, output_dir)

    if not os.path.isdir(output_dir_full):
        os.mkdir(output_dir_full)


def compile(input_dir: str, output_dir: str):
    try:
        validate_paths(input_dir, output_dir)
    except FileNotFoundError as error:
        print(error, file=sys.stderr, flush=True)

    formatter = bs4.formatter.HTMLFormatter(indent=4)
    input_dir_full = os.path.join(ROOT_DIR, input_dir)

    for filepath in glob.iglob(input_dir_full + "**/**", recursive=True):
        if not os.path.isfile(filepath):
            continue

        if filepath.find(partial_infix) != -1:
            continue

        content = resolve_template(filepath, input_dir)
        filepath_out = os.path.join(ROOT_DIR, output_dir, os.path.basename(filepath))

        with open(filepath_out, "w") as file:
            content_pretty = BeautifulSoup(content, "html.parser").prettify(formatter=formatter)

            if isinstance(content_pretty, bytes):
                content_pretty = content_pretty.decode("utf-8")

            file.write(str(content_pretty))


def resolve_template(template_path, input_dir, visited=None, cache=None):
    if visited is None:
        visited = set()

    if cache is None:
        cache = {}

    if template_path in visited:
        raise ValueError("Cyclic reference detected.")

    content = load_template(template_path)

    def pull_replacer(match_result: re.Match):
        pulled_template = match_result.group(1)
        pulled_template = os.path.join(os.path.dirname(template_path), pulled_template)
        return resolve_template(pulled_template, input_dir, visited.copy(), cache.copy())

    return re.sub(pull_pattern, pull_replacer, content)


def load_template(template_path: str) -> str:
    try:
        with open(template_path) as file:
            return file.read()
    except FileNotFoundError:
        return "[[ MISSING TEMPLATE ]]"
