#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

mkdir -p "$workdir/admin" "$workdir/DSCI_523"
cp "$repo_root/admin/sync_course_repos.sh" "$workdir/admin/"

src="$workdir/source"
remote="$workdir/remotes/DSCI_523_demo.git"
git init -q "$src"
git -C "$src" config user.email test@example.com
git -C "$src" config user.name "Sync Routing Test"
printf 'demo\n' > "$src/README.md"
git -C "$src" add README.md
git -C "$src" commit -q -m init
git clone -q --bare "$src" "$remote"

cat > "$workdir/admin/sources.conf" <<EOF
# name ; api_base ; org ; include ; exclude ; family ; mode
current ; https://api.invalid ; ignored ; ; ; current ; mirror
EOF
printf 'file://%s\n' "$remote" > "$workdir/admin/current.txt"

mkdir -p "$workdir/resources"
touch "$workdir/resources/mds-2026-27.txt" "$workdir/resources/ubc-mds.txt"

list_output="$workdir/list-only.log"
if ! (cd "$workdir" && bash admin/sync_course_repos.sh --offline --list-only >"$list_output" 2>&1); then
  cat "$list_output"
  exit 1
fi

for old_root in resources/mds-2026-27 resources/ubc-mds assignments; do
  if [[ -e "$workdir/$old_root" ]]; then
    echo "old clone root was created during list-only: $old_root" >&2
    exit 1
  fi
done

touch "$workdir/resources/mds-2026-27.txt" "$workdir/resources/ubc-mds.txt"

sync_output="$workdir/offline-sync.log"
if ! (cd "$workdir" && bash admin/sync_course_repos.sh --offline current >"$sync_output" 2>&1); then
  cat "$sync_output"
  exit 1
fi

expected="$workdir/DSCI_523/official/current/DSCI_523_demo"
unrouted="$workdir/admin/current/DSCI_523_demo"
if [[ ! -d "$expected/.git" ]]; then
  echo "expected routed clone at: $expected" >&2
  if [[ -d "$unrouted/.git" ]]; then
    echo "found unrouted clone at: $unrouted" >&2
  fi
  cat "$sync_output"
  exit 1
fi

if [[ -e "$unrouted" ]]; then
  echo "unrouted clone root was created: $unrouted" >&2
  exit 1
fi

cat "$list_output"
cat "$sync_output"
echo "offline list-only and sync routing used admin family snapshots and course roots"
