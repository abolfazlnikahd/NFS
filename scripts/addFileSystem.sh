#!/bin/sh
lvcreate -L $1\G -n $2 $3
mkfs.  