from flask import Flask, request, send_file, render_template
from PIL import Image
import io
import os

app = Flask(__name__)

BANNER_PATH = os.path.join(os.path.dirname(__file__), "static", "banner.png")
SIZE = 1000
BANNER_RATIO = 0.22


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return "画像がありません", 400

    file = request.files["image"]
    if file.filename == "":
        return "ファイルを選択してください", 400

    product = Image.open(file.stream).convert("RGB")
    banner = Image.open(BANNER_PATH).convert("RGB")

    banner_h = int(SIZE * BANNER_RATIO)
    product_h = SIZE - banner_h

    canvas = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    canvas.paste(product.resize((SIZE, product_h), Image.LANCZOS), (0, 0))
    canvas.paste(banner.resize((SIZE, banner_h), Image.LANCZOS), (0, product_h))

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=95)
    buf.seek(0)

    return send_file(buf, mimetype="image/jpeg", as_attachment=True, download_name="ebay_listing.jpg")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
