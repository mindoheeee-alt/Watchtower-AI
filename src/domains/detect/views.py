import io
import tempfile

import cv2
import numpy as np
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    Response,
)

from src.domains.detect.detector import (
    detector_models,
    DetectorEnum,
)
from src.domains.detect.forms import UploadImageForm, UploadVideoForm

detect_views = Blueprint(
    "detect", __name__, template_folder="templates", static_folder="static"
)


@detect_views.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@detect_views.route("/images", methods=["GET", "POST"])
def detect_images():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        selected_detector = form.model.data
        if selected_detector not in [de.value for de in DetectorEnum]:
            return "잘못된 모델입니다.", 400
        model = detector_models[DetectorEnum(selected_detector)]()
        results = model.detect(img, conf=0.5)

        return ndarray_to_image_bytes(results[0].plot())
    form.model.data = DetectorEnum.FireDetectV1.value
    return render_template("detect/detect_images.html", form=form)


@detect_views.route("/videos", methods=["GET", "POST"])
def detect_videos():
    form = UploadVideoForm()
    if form.validate_on_submit():
        file = form.video.data

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        cap = cv2.VideoCapture(tmp_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter.fourcc(*"avc1")
        out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

        selected_detector = form.model.data
        if selected_detector not in [de.value for de in DetectorEnum]:
            return "잘못된 모델입니다.", 400
        model = detector_models[DetectorEnum(selected_detector)]()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.detect(frame, conf=0.5, verbose=False)

            out.write(results[0].plot())

        cap.release()
        out.release()

        return Response(generate("output.mp4"), mimetype="video/mp4")

    form.model.data = DetectorEnum.FireDetectV1.value
    return render_template("detect/detect_videos.html", form=form)


def generate(filename: str):
    out_buffer = io.BytesIO()

    with open(filename, "rb") as f:
        out_buffer.write(f.read())

    out_buffer.seek(0)
    while True:
        data = out_buffer.read(1024 * 1024)
        if not data:
            break
        yield data


def ndarray_to_image_bytes(array: np.ndarray):
    success, encoded = cv2.imencode(".png", array)
    if not success:
        return "Encode error", 500

    img_bytes = encoded.tobytes()
    return Response(img_bytes, mimetype="image/png")
