from flask import Flask, render_template, request, redirect, url_for
import os,cv2

app = Flask(__name__)
app.config['TOPS_UPLOAD_FOLDER'] = os.path.join('static', 'tops')
app.config['PANTS_UPLOAD_FOLDER'] = os.path.join('static', 'pants')

# Create upload folders if they don't exist
os.makedirs(app.config['TOPS_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PANTS_UPLOAD_FOLDER'], exist_ok=True)

def remove_background(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(image, image, mask=mask_inv)
    return foreground

@app.route('/')
def index():
    tops = os.listdir(app.config['TOPS_UPLOAD_FOLDER'])
    pants = os.listdir(app.config['PANTS_UPLOAD_FOLDER'])
    return render_template('index.html', tops=tops, pants=pants)

@app.route('/upload/tops', methods=['POST'])
def upload_tops():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['TOPS_UPLOAD_FOLDER'], filename))
        input_image = os.path.join(app.config['TOPS_UPLOAD_FOLDER'],filename)
        output_image = os.path.join(app.config['TOPS_UPLOAD_FOLDER'],"bgrm"+filename)
        result = remove_background(input_image)
        cv2.imwrite(output_image, result)
        os.remove(os.path.join(app.config['TOPS_UPLOAD_FOLDER'],filename))
        return redirect(url_for('index'))

@app.route('/upload/pants', methods=['POST'])
def upload_pants():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['PANTS_UPLOAD_FOLDER'], filename))
        input_image = os.path.join(app.config['PANTS_UPLOAD_FOLDER'],filename)
        output_image = os.path.join(app.config['PANTS_UPLOAD_FOLDER'],"bgrm"+filename)
        result = remove_background(input_image)
        cv2.imwrite(output_image, result)
        os.remove(os.path.join(app.config['PANTS_UPLOAD_FOLDER'],filename))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
