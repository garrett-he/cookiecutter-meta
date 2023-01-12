from pytest_cookies.plugin import Cookies

from .helper import LICENSE_SPEC, generate_cookiecutter_context


def test_bake_readme(cookies: Cookies):
    for license_id, license_spec in LICENSE_SPEC.items():
        context = generate_cookiecutter_context()
        context['license_id'] = license_id

        result = cookies.bake(extra_context=context)
        assert not result.exception

        readme = result.project_path.joinpath('README.md').read_text()
        assert context['project_name'] in readme
        assert context['project_description'] in readme

        assert license_spec['stub'] in readme

        if license_id == 'Unlicense':
            assert 'This is free and unencumbered software released into the public domain' in readme
        else:
            assert f'Copyright (C) {context["license_year"]} {context["license_fullname"]}' in readme
            assert f'see [{license_spec["filename"]}](./{license_spec["filename"]}).' in readme
