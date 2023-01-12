import random

from chance import chance

LICENSE_SPEC = {
    'Apache-2.0': {'filename': 'LICENSE', 'stub': 'Apache License', 'has_author': False},
    'BSD-3-Clause': {'filename': 'LICENSE', 'stub': 'BSD 3-Clause License', 'has_author': True},
    'GPL-3.0': {'filename': 'COPYING', 'stub': 'GNU General Public License', 'has_author': False},
    'LGPL-3.0': {'filename': 'COPYING', 'stub': 'GNU Lesser General Public License', 'has_author': False},
    'MIT': {'filename': 'LICENSE', 'stub': 'MIT License', 'has_author': True},
    'MPL-2.0': {'filename': 'LICENSE', 'stub': 'Mozilla Public License', 'has_author': False},
    'Unlicense': {'filename': 'UNLICENSE', 'stub': 'This is free and unencumbered software released into the public domain', 'has_author': False}
}


def generate_cookiecutter_context() -> dict:
    return {
        'project_name': f'{chance.word().capitalize()} {chance.word().capitalize()}',
        'project_slug': f'{chance.word().lower()}-{chance.word().lower()}',
        'project_description': chance.sentence(),
        'author_name': chance.name(),
        'author_email': chance.email(),
        'license_id': chance.pickone(list(LICENSE_SPEC.keys())),
        'license_fullname': f'{chance.name()} <{chance.email()}>',
        'license_year': str(random.randint(2000, 2023)),
        'github_path': f'{chance.word()}/{chance.word()}-{chance.word()}'.lower()
    }
