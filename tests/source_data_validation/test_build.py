import json
import os
import shutil
from pathlib import Path

import pytest
from jsonschema import RefResolver, validate

from tests.source_data_validation import (
    REMOTE_CONFIGURATIONS_V1_SCHEMA,
    REMOTE_CONFIGURATIONS_V2_SCHEMA,
    SCHEMAS,
)


@pytest.fixture(autouse=True)
def build_run_and_teardown():
    os.system("python build.py 1.0.0")
    yield
    shutil.rmtree("build", ignore_errors=True)


def test_build_successful():
    assert os.path.exists("build/v2")
    assert os.path.exists("build/v1/rules.json")


def test_built_v1_remote_configurations_schema():
    schema = json.loads(REMOTE_CONFIGURATIONS_V1_SCHEMA.read_text())
    remote_config = json.loads(Path("build/v1/rules.json").read_text())
    resolver = RefResolver(f"file://{SCHEMAS}/", schema)
    validate(remote_config, schema, resolver=resolver)


def test_built_v2_remote_configurations_schema():
    schema = json.loads(REMOTE_CONFIGURATIONS_V2_SCHEMA.read_text())
    resolver = RefResolver(f"file://{SCHEMAS}/", schema)
    for remote_config in Path("build/v2").rglob("*.json"):
        rules = json.loads(remote_config.read_text())
        validate(rules, schema, resolver=resolver)
