#!/usr/bin/env bash
set -e

pip install -r requirements.txt

curl -fsSL https://deno.land/install.sh | sh

export DENO_INSTALL="/opt/render/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"

deno --version
