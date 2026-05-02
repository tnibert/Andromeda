#! /bin/bash
pytest -q core/test_observe.py
pytest -q core/test_scene.py
pytest -q core/test_timer.py
pytest -q core/test_gameobject.py
pytest -q core/test_statemachine.py
