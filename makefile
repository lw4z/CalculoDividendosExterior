start:
	streamlit run view/-\ ⌂\ Início.py & uvicorn main:app --reload

full_test:
	pytest -v

setup:
	pip install -r requirements.txt
