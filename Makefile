build:
	@docker build -t coaching-backend .
	@docker rm -f coaching-backend
	@docker run -itd --name coaching-backend -p 8000:8000 coaching-backend
