from glob import glob

from pytest_cookies.plugin import Cookies

from .helper import LICENSE_SPEC, generate_cookiecutter_context


def test_bake_licenses_and_readme(cookies: Cookies):
    for license_id, license_spec in LICENSE_SPEC.items():
        context = generate_cookiecutter_context()
        context['license_id'] = license_id

        result = cookies.bake(extra_context=context)
        assert not result.exception

        license_text = result.project_path.joinpath(license_spec['filename']).read_text(encoding='utf-8')
        assert license_spec['stub'] in license_text

        if license_spec['has_author']:
            assert context['license_fullname'] in license_text
            assert context['license_year'] in license_text

        assert len(glob('LICENSE.*')) == 0
        print(license_id)

        match license_id:
            case 'GPL-3.0' | 'LGPL-3.0':
                assert result.project_path.joinpath('COPYING').exists()
                assert not result.project_path.joinpath('LICENSE').exists()
                assert not result.project_path.joinpath('UNLICENSE').exists()
            case 'Unlicense':
                assert not result.project_path.joinpath('COPYING').exists()
                assert not result.project_path.joinpath('LICENSE').exists()
                assert result.project_path.joinpath('UNLICENSE').exists()
            case _:
                assert not result.project_path.joinpath('COPYING').exists()
                assert result.project_path.joinpath('LICENSE').exists()
                assert not result.project_path.joinpath('UNLICENSE').exists()

        readme = result.project_path.joinpath('README.md').read_text()
        assert context['template_name'] in readme
        assert context['template_description'] in readme
        assert f'cookiecutter gh:{context["github_path"]}' in readme

        assert license_spec['stub'] in readme

        if license_id == 'Unlicense':
            assert 'This is free and unencumbered software released into the public domain' in readme
        else:
            assert f'Copyright (C) {context["license_year"]} {context["license_fullname"]}' in readme
            assert f'see [{license_spec["filename"]}](./{license_spec["filename"]}).' in readme
