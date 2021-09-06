
How to update and upload a version
==================================

```bash
bumpversion --current-version 1.0.1 patch setup.py votesim/__init__.py

python setup.py sdist bdist_wheel
twine upload dist/* -u jont
git commit
git tag v1.0.2
git push origin v1.0.2
```
