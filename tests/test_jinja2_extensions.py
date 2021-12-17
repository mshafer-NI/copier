import json

from jinja2.ext import Extension

import copier

from .helpers import PROJECT_TEMPLATE, build_file_tree


class FilterExtension(Extension):
    """Jinja2 extension to add a filter to the Jinja2 environment."""

    def __init__(self, environment):
        super().__init__(environment)

        def super_filter(obj):
            return str(obj) + " super filter!"

        environment.filters["super_filter"] = super_filter


class GlobalsExtension(Extension):
    """Jinja2 extension to add global variables to the Jinja2 environment."""

    def __init__(self, environment):
        super().__init__(environment)

        def super_func(argument):
            return str(argument) + " super func!"

        environment.globals.update(super_func=super_func)
        environment.globals.update(super_var="super var!")


def test_default_jinja2_extensions(tmp_path):
    copier.copy(
        str(PROJECT_TEMPLATE) + "_extensions_default",
        tmp_path,
    )
    super_file = tmp_path / "super_file.md"
    assert super_file.exists()
    expected = "path\n"
    assert super_file.read_text() == expected


def test_additional_jinja2_extensions(tmp_path):
    copier.copy(
        str(PROJECT_TEMPLATE) + "_extensions_additional",
        tmp_path,
    )
    super_file = tmp_path / "super_file.md"
    assert super_file.exists()
    expected = "super var! super func! super filter!\n"
    assert super_file.read_text() == expected


def test_to_json_filter_with_conf(tmp_path_factory):
    template = tmp_path_factory.mktemp("template")
    project = tmp_path_factory.mktemp("project")
    build_file_tree(
        {
            template / "conf.json.jinja": "{{ _copier_conf|to_json }}",
        }
    )
    copier.copy(
        str(template),
        project,
    )
    conf_file = project / "conf.json"
    assert conf_file.exists()
    # must not raise an error
    json.loads(conf_file.read_text())
