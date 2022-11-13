install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black --line-length 80 *.py

lint:
	print("Skipping manually for now...") #flake8 --ignore E501,W291,E203 *.py

run:
	streamlit run app.py

ci: format lint
