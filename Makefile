.PHONY: build run dev pull-model create-model push-model

# Build and create the Ollama model
build: create-model

# Run the full application with Docker
run:
	docker-compose up --build

# Run in development mode (requires local Ollama)
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Pull the model from Ollama registry
pull-model:
	ollama pull yconcept/y-nav

# Create the model locally
create-model:
	ollama create y-nav -f Modelfile

# Push model to registry (requires login)
push-model:
	ollama push yconcept/y-nav

# Clean up Docker containers
clean:
	docker-compose down

# Install Python dependencies
install:
	pip install -r requirements.txt
