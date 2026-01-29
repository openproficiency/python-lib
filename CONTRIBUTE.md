## Verifying tests and coverage

## Run Tests workflow

Before creating a workflow, please run the [Unit Tests](./.github/workflows/unit-tests.yml) workflow locally using Act.

```bash
act --job verify_unit_tests
```

```bash
act -W .github/workflows/unit-tests.yml --job verify_unit_tests
```

## Publish to PyPI

1. Install tooling (run from the repo root).

   ```bash
   python3 -m pip install --upgrade build twine
   ```

2. Clean old artifacts.

   ```bash
   rm -rf dist build *.egg-info
   ```

3. Build the package (creates sdist and wheel in `dist/`).

   ```bash
   python3 -m build
   ```

4. Validate metadata (confirm long description renders).

   ```bash
   python3 -m twine check dist/*
   ```

5. Upload to PyPI. Twine will prompt for a password. Use your PyPI API token.

   ```bash
   python3 -m twine upload dist/*
   ```
