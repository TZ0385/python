# Task contract: release-evidence builder (ship check)

Change only `starter/ship_check.py`. Standard library only. Never modify the
scenario projects except through copies.

- `run_checks(command, cwd) -> dict`: run `[sys.executable, *command]` in
  *cwd*, capture output, and return
  `{"command": " ".join(command), "exit_code": int, "ran": int, "result": str}`:
  - `ran` is the test count parsed from `Ran N tests in ...`.
  - `result` is `"no-tests"` when `ran == 0` (regardless of exit code —
    modern Pythons exit nonzero for "NO TESTS RAN"), `"failed"` when the
    exit code is nonzero, otherwise `"ok"`.
- `build_record(checks, *, verified_on, unverified=None) -> dict`:
  `{"verified_on", "checks", "all_passed", "unverified"}` where
  `all_passed` is true only when every check has exit code 0 AND result
  `"ok"` (zero-test projects never pass), and `unverified` defaults to an
  empty list.
- `write_record(record, destination)`: write JSON (UTF-8, indent 2, trailing
  newline) atomically via a sibling temp file plus `os.replace`; create
  missing parent directories; never leave a `.tmp` file on success.
- `run_project(project_dir, *, verified_on) -> dict`: read `ship.json`
  (`command`, optional `unverified`), run the checks in the project
  directory, build the record, write `SHIP-RECORD.json` there, return it.
- `main(argv=None) -> int`:
  - `ship_check.py <project-dir> [--verified-on YYYY-MM-DD]`; otherwise
    print usage to stderr and return 2. Without `--verified-on` use today's
    date.
  - Print `all_passed=... checks=...` to stdout; return 0 when
    `all_passed`, otherwise 1.

Done means `python verify.py starter` exits 0 with all ten tests passing.
