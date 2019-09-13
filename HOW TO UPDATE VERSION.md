
How to update and upload a version
==================================

```bash
bumpversion --current-version 0.1.3 patch setup.py pyrankvote/__init__.py
git tag 0.1.4
python setup.py sdist bdist_wheel
twine upload dist/* -u jont

```


