tf='.env'

rm -rf $tf
virtualenv $tf -p python3
$tf/bin/pip install -e fortunate

export FORTUNATE_SETTINGS=dev_settings.py

