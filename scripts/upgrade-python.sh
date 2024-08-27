#!/bin/bash
find ./src -name '*.py' -exec pyupgrade --py310 --py311 {} +
find ./tests -name '*.py' -exec pyupgrade --py310 --py311 {} +
