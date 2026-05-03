#! /bin/bash
# must run from root directory of repository
source .venv/bin/activate
export PYTHONPATH=.
pytest -q core/test_observe.py
pytest -q core/test_scene.py
pytest -q core/test_timer.py
pytest -q core/test_gameobject.py
pytest -q core/test_statemachine.py
deactivate
