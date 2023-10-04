import random
from glob import glob

from chance import chance
from pytest_cookies.plugin import Cookies

license_stubs = {
    'Apache-2.0': 'Apache License',
    'BSD-3-Clause': 'BSD 3-Clause License',
    'GPL-3.0': 'GNU General Public License',
    'LGPL-3.0': 'GNU Lesser General Public License',
    'MIT': 'MIT License',
    'MPL-2.0': 'Mozilla Public License'
}


def test_create_project(cookies: Cookies):
    result = cookies.bake()
    assert not result.exception

    assert result.project_path.joinpath('.editorconfig').exists()


def generate_context() -> dict:
    return {
        'project_name': f'{chance.word().capitalize()} {chance.word().capitalize()}',
        'project_slug': f'{chance.word().lower()}-{chance.word().lower()}',
        'project_description': chance.sentence(),
        'author_name': chance.name(),
        'author_email': chance.email(),
        'license_id': chance.pickone([key for key in license_stubs.keys()]),
        'license_fullname': f'{chance.name()} <{chance.email()}>',
        'license_year': str(random.randint(2000, 2023))
    }


def test_bake_license(cookies: Cookies):
    for license_id, license_stub in license_stubs.items():
        context = generate_context()
        context['license_id'] = license_id

        result = cookies.bake(extra_context=context)
        assert not result.exception

        license_text = result.project_path.joinpath('LICENSE').read_text(encoding='utf-8')
        assert license_stub in license_text

        assert len(glob('LICENSE.*')) == 0
        assert not result.project_path.joinpath('UNLICENSE').exists()

        if license_id in ['BSD-3-Clause', 'MIT']:
            assert context['license_fullname'] in license_text
            assert context['license_year'] in license_text

        readme = result.project_path.joinpath('README.md').read_text(encoding='utf-8')

        assert context['project_name'] in readme
        assert context['project_description'] in readme

        assert f'Copyright (C) {context["license_year"]} {context["license_fullname"]}' in readme
        assert license_stubs[context['license_id']] in readme
        assert 'see [LICENSE](./LICENSE)' in readme

    context = generate_context()
    context['license_id'] = 'Unlicense'
    result = cookies.bake(extra_context=context)
    assert not result.exception
    assert len(glob('LICENSE.*')) == 0
    assert not result.project_path.joinpath('LICENSE').exists()

    unlicense_text = result.project_path.joinpath('UNLICENSE').read_text(encoding='utf-8')
    assert 'This is free and unencumbered software released into the public domain' in unlicense_text
    assert context['license_fullname'] not in unlicense_text
    assert context['license_year'] not in unlicense_text

    readme = result.project_path.joinpath('README.md').read_text(encoding='utf-8')
    assert 'This is free and unencumbered software released into the public domain' in readme
    assert 'see [UNLICENSE](./UNLICENSE)' in readme
