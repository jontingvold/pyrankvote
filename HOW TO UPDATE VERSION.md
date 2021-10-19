
How to update and upload a version
==================================

```bash
CURRENT_VERSION=$(python -c 'import pyrankvote;print(pyrankvote.__version__)')
bumpversion --current-version CURRENT_VERSION patch setup.py pyrankvote/__init__.py
NEW_VERSION=$(python -c 'import pyrankvote;print(pyrankvote.__version__)')

python setup.py sdist bdist_wheel
twine upload dist/* -u jont
git commit
git tag v$NEW_VERSION
git push origin v$NEW_VERSION
```

