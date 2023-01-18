#!/bin/bash
set -u

IMAGE="${IMAGE}"
ENVFILE="${ENVFILE-.env}"
TMPDIR="${TMPDIR-/tmp/garmin}"

exec docker run --env-file=${ENVFILE} -v ${TMPDIR}:/data -ti ${IMAGE} $@
