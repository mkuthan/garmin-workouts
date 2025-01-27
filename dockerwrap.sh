#!/bin/bash
set -u

IMAGE="${IMAGE}"
ENVFILE="${ENVFILE-.env}"
TMPDIR="${TMPDIR-/tmp/garmin}"
DATADIR="${DATADIR-./}"
exec docker run --env-file=${ENVFILE} -v ${TMPDIR}:/tmp -v ${DATADIR}:/data/ -ti ${IMAGE} $@
