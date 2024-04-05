run:
	granian --interface asgi main:app --port 8000 --reload

save-pip:
	pip freeze > requirements.txt