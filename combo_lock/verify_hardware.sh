!#/bin/bash

cd /var/lib/cloud9/ENGI301/python/combo_lock
python3 ht16k33.py

cd /sys/class/gpio/gpio59
cat direction
cat value

