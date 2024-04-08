run:
	granian --interface asgi main:app --port 8000

save-pip:
	pip freeze > requirements.txt