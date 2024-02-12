from flask import Flask, render_template, request, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
# Assuming validate_configuration_against_matrix is in a file named csv_validate.py
from csv_validate import validate_configuration_against_matrix

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        config_file = request.files['file']
        matrix_file = request.files['existing_yaml']

        if config_file and matrix_file:
            # Generate a temporary file to store the report
            temp_file_path = os.path.join(tempfile.gettempdir(), 'validation_report.csv')

            # Process and validate the uploaded files
            report_df = validate_configuration_against_matrix(config_file, matrix_file)
            report_df.to_csv(temp_file_path, index=False)

            # Send the result file
            return send_file(temp_file_path, as_attachment=True, attachment_filename='validation_report.csv', cache_timeout=0)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
