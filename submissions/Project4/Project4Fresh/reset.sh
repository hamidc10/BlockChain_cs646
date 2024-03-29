#!/usr/bin/env bash

# Script to reset nodes / delete all transactions and blocks

rm -f ./*.json

rm -rf node1/*.log
rm -rf node1/*.json
rm -rf node1/blocks/
rm -rf node1/pending/
rm -rf node1/processed/
rm -rf node1/rejected/

rm -rf node2/*.log
rm -rf node2/*.json
rm -rf node2/blocks/
rm -rf node2/pending/
rm -rf node2/processed/
rm -rf node2/rejected/

rm -rf node3/*.log
rm -rf node3/*.json
rm -rf node3/blocks/
rm -rf node3/pending/
rm -rf node3/processed/
rm -rf node3/rejected/
