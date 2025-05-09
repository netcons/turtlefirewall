#!/usr/bin/env bash
sed -n "s/^PACKAGE_VERSION=.*'\(.*\)'.*/\1/p" configure
