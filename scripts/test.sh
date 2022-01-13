#!/bin/bash

coverage run -m unittest discover -v
exit_code=$?
coverage html -d /tmp/alphasea-example-model/htmlcov

exit $exit_code
