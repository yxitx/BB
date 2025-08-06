from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def dummy_predict(image):
    # 这里是占位的AI预测函数，返回原图
    return image

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        image = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

    result_img = dummy_predict(image)

    # 保存结果图
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
    result_img.save(result_path)

    return jsonify({'result_url': f'/static/uploads/result.jpg'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
