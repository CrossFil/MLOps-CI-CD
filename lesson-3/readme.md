# MLOps Lesson 3: Docker Optimization & Compose

## Task Objective: Create a script to install Docker, Docker Compose, Python, and ML dependencies, then containerize a model with size optimization.

### 1. Quick Start
- Environment Setup: chmod +x install_dev_tools.sh && ./install_dev_tools.sh

- Prepare Model: python3 export_model.py

- Run via Docker Compose: docker-compose run classifier

### 2. Performance Comparison
- Fat Image: 8.53 GB (Full Python base)
- Slim Image: 1.10 GB (Multi-stage + CPU-only Torch)

- Key Achievement: Reduced image size by 87% (7.4 GB saved) using multi-stage builds.

### 3. Repository Structure
- install_dev_tools.sh: Automated environment setup script.

- docker-compose.yml: Orchestration for easy container launch.

- inference.py: Image classification script.

- Dockerfile.slim: Optimized production-ready image.

- comparison.txt: Image size analysis report.
