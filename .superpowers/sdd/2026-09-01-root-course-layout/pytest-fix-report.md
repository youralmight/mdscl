# Pytest discovery fix report

## RED

Existing controller log showed `uv run pytest` was collecting tests from ignored upstream course-clone material and failing on dependencies that are not part of this package:

```text
tmp/runs/20260902-controller-final/logs/pytest.log
collected 4 items / 3 errors
ERROR admin/upstream/public/DSCI_532_vis-2_book/code/lecture05/demo01/test_extra_instructions.py
E   ModuleNotFoundError: No module named 'querychat'
ERROR admin/upstream/public/DSCI_532_vis-2_book/code/lecture08/testing/test_app04_playwright.py
E   ModuleNotFoundError: No module named 'shiny'
```

## Change

- Added pytest discovery excludes in `pyproject.toml` for:
  - `admin/upstream`
  - `DSCI_*/official`
  - `DSCI_*/assignments`
  - `COLX_*/official`
  - `COLX_*/assignments`
- Added one repository-owned smoke test for `mdscl.main()` because, after excluding course/upstream clone tests, the package had no pytest-owned tests and bare `uv run pytest` exits non-zero on zero collected tests.

## GREEN

```text
$ uv run pytest
collected 1 item
admin/python/tests/test_mdscl.py .                                       [100%]
1 passed in 0.03s
```

Full log: `tmp/runs/20260902-pytest-discovery-fix/logs/uv-run-pytest-green.log`

## CLI smoke

```text
$ uv run mdscl
Hello from mdscl!
```

Full log: `tmp/runs/20260902-pytest-discovery-fix/logs/uv-run-mdscl.log`
