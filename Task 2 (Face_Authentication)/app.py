from fastapi import FastAPI, UploadFile, File, HTTPException
from insightface.app import FaceAnalysis
import cv2
import numpy as np

app = FastAPI(
    title="Face Verification API"
)

# Initialize InsightFace
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0, det_size=(640, 640))


def read_image(file_bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def cosine_similarity(emb1, emb2):
    emb1 = emb1 / np.linalg.norm(emb1)
    emb2 = emb2 / np.linalg.norm(emb2)

    return float(np.dot(emb1, emb2))


@app.post("/verify")
async def verify_faces(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    img1 = read_image(await image1.read())
    img2 = read_image(await image2.read())

    faces1 = face_app.get(img1)
    faces2 = face_app.get(img2)

    if len(faces1) == 0:
        raise HTTPException(
            status_code=400,
            detail="No face detected in image1"
        )

    if len(faces2) == 0:
        raise HTTPException(
            status_code=400,
            detail="No face detected in image2"
        )

    # Take first detected face
    face1 = faces1[0]
    face2 = faces2[0]

    embedding1 = face1.embedding
    embedding2 = face2.embedding

    similarity = cosine_similarity(
        embedding1,
        embedding2
    )

    # Threshold can be tuned
    threshold = 0.50

    result = (
        "same person"
        if similarity >= threshold
        else "different person"
    )

    return {
        "verification_result": result,
        "similarity_score": round(similarity, 4),
        "bounding_boxes": {
            "image1": face1.bbox.astype(int).tolist(),
            "image2": face2.bbox.astype(int).tolist()
        }
    }