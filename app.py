from flask import Flask, render_template, request, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
from csv-validate import validate_configuration_against_matrix  # Ensure this is correctly imported

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the files part
        if 'file' not in request.files or 'existing_yaml' not in request.files:
            return 'No file part', 400
        
        file = request.files['file']
        existing_yaml = request.files['existing_yaml']

        if file.filename == '' or existing_yaml.filename == '':
            return 'No selected file', 400

        if file and existing_yaml:
            # Secure the filenames
            filename = secure_filename(file.filename)
            yaml_filename = secure_filename(existing_yaml.filename)

            # Create temporary files
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, filename)
            yaml_path = os.path.join(temp_dir, yaml_filename)
            output_path = os.path.join(temp_dir, "validation_report.csv")

            file.save(file_path)
            existing_yaml.save(yaml_path)

            # Run the validation
            validate_configuration_against_matrix(file_path, yaml_path, output_path)

            # Remove uploaded files
            os.remove(file_path)
            os.remove(yaml_path)

            # Send the result file
            return send_file(output_path, as_attachment=True, attachment_filename='validation_report.csv')

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
