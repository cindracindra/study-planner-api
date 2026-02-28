#! /bin/bash

ABC_DOCS="https://abc-api.doc.ic.ac.uk/openapi.json"
ABC_SCHEMAS_FILE="app/doc_upstream_services/abc/schemas.py"

datamodel-codegen \
	--url $ABC_DOCS \
	--input-file-type openapi \
	--target-python-version 3.13 \
	--use-standard-collections \
	--use-union-operator \
	--use-double-quotes \
	--disable-future-imports \
	--disable-timestamp \
	--output $ABC_SCHEMAS_FILE

if ! git diff --quiet "$ABC_SCHEMAS_FILE"
then
    echo "Generated ABC schemas differ from committed version. Please review and commit."
    exit 1
fi
