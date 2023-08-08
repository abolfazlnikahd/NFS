#!/bin/sh
pvcreate $1
vgcreate $2 $1
exit 0