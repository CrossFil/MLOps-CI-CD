# ML Inference Service: Docker Optimization

## This repository contains a PyTorch-based image classification service optimized for production using Docker.

### 1. Quick Start
- Environment Setup: chmod +x install_dev_tools.sh && ./install_dev_tools.sh

- Prepare Model: python3 export_model.py

- Run Optimized Docker: docker build -t ml-slim -f Dockerfile.slim . docker run --rm -v $(pwd):/app ml-slim example.jpg

### 2. Performance Comparison
- Fat Image: 8.53 GB (Standard Python base)
- Slim Image: 1.10 GB (Multi-stage + CPU-only Torch)

Key Achievement: Reduced image size by 87% (7.4 GB saved) using multi-stage builds and specialized PyTorch distributions.

### 3. Repository Structure
- inference.py: Top-3 prediction script.

- export_model.py: TorchScript model exporter.

- Dockerfile.slim: Optimized multi-stage build.

- comparison.txt: Full optimization report.
