# Runs .github/workflows/pr_check.yml locally
python3 -m unittest discover -s src -v
uv run black --check $(git ls-files '*.py')
uv run pylint $(git ls-files '*.py')