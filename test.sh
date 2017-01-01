tf='.venv_test'

virtualenv $tf -p python
$tf/bin/pip install -e fortunate

export FORTUNATE_SETTINGS=test_settings.py
$tf/bin/python -m fortunate.tests
unset FORTUNATE_SETTINGS

rm -rf $tf
