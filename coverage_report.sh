#!/bin/bash

coverage run -m unittest

coverage report --omit "venv/*"
