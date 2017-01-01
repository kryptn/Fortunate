tf='.env'

rm -rf $tf
virtualenv $tf -p python
$tf/bin/pip install -e fortunate


