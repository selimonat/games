setup: setup.pip setup.poetry 

setup.pip:
	pip install --upgrade pip
	pip install "poetry==1.0.3"

setup.poetry:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry config repositories.freenow_artifactory https://repos.mytaxi.com/artifactory/api/pypi/pypi/simple
	poetry config http-basic.freenow_artifactory data-science.service AKCp5ccbGTAg6DriC9xjZnHyH4tBHjeXfkg1xEvnfMaMgYKb1h1RWsPJ2QXT2wyovS1VBiBtP
	poetry install --no-interaction --no-ansi
