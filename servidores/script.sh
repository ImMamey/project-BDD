#!/bin/bash

python /usr/app/src/servidor_A.py >/proc/1/fd/1 2>/proc/1/fd/2 &
python /usr/app/src/servidor_B.py >/proc/1/fd/1 2>/proc/1/fd/2