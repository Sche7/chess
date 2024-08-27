#!/bin/bash
find ./src -name '*.py' -exec pyupgrade --py310 {} +
