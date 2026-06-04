# Assignment Submission

## Overview

This submission contains two tasks:

1. **Amazon Product Scraper**
2. **Face Authentication (Face Verification) API**

---

# Task 1: Amazon Scraper

## Objective

Python script that scrapes laptop product information from Amazon.in and stores the results in a CSV file with a timestamped filename.

## Extracted Information

The scraper collects the following details:

* Product Title
* Product Image URL
* Product Rating
* Product Price
* Ad / Organic Result

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Pandas

## Installation

Install the required dependencies:

```bash
pip install requests beautifulsoup4 pandas
```

## Running the Script

Execute the script:

```bash
python amazon_scraper.py
```

## Output

A timestamped CSV file will be generated in the project directory.

Example:

```text
amazon_laptops_20260604_143501.csv
```

---

# Task 2: Face Authentication (Face Verification) API

## Objective

Build a FastAPI service that verifies whether two face images belong to the same person.

## Features

* Accepts two face images
* Detects faces in both images
* Extracts facial embeddings using InsightFace
* Computes cosine similarity
* Returns:

  * Verification result
  * Similarity score
  * Face bounding boxes

## Technologies Used

* Python
* FastAPI
* InsightFace
* OpenCV
* NumPy
* ONNX Runtime

## Installation

Install the required dependencies:

```bash
pip install fastapi uvicorn insightface opencv-python numpy python-multipart onnxruntime
```

## Running the API

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoint

### POST /verify

Uploads two face images and performs face verification.

### Response Example

```json
{
  "verification_result": "same person",
  "similarity_score": 0.83,
  "bounding_boxes": {
    "image1": [132, 85, 321, 290],
    "image2": [125, 92, 315, 288]
  }
}
```

## Verification Process

1. Face detection is performed on both images.
2. Facial embeddings are extracted.
3. Cosine similarity is calculated between embeddings.
4. A threshold is applied to determine whether the faces belong to the same person.
