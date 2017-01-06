tf='.venv_test'

virtualenv $tf -p python
$tf/bin/pip install -e fortunate
$tf/bin/python fortunate/setup.py test

rm -rf $tf
