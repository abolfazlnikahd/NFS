#!/bin/sh
wipefs -a $1
yes | lvremove $1
