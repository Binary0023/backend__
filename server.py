from flask import Flask, request, send_file, jsonify
import os
import pikepdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "PDF Compression API is running!"})

@app.route("/compress", methods=["POST"])
def compress_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    pdf_file = request.files["pdf"]
    
    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save original file
    input_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(input_path)

    # Compressed file path
    compressed_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{pdf_file.filename}")

    try:
        # Open the PDF and compress it
        pdf = pikepdf.open(input_path)
        pdf.save(compressed_path, optimize=True)

        # Return compressed file
        return send_file(compressed_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Compression failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
