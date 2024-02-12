import pandas as pd

def validate_configuration_against_matrix(config_file_stream, matrix_file_stream):
    # Convert the file streams to pandas DataFrames
    config_df = pd.read_csv(config_file_stream)
    matrix_df = pd.read_csv(matrix_file_stream, index_col=0)
    
    # Preparing a list of boolean fields for special handling
    boolean_fields = ['http_2xx', 'icmp', 'ssh-banner', 'tcp-connect', 'SNMP', 'Exporter_SSL']
    
    # Prepare a report DataFrame to track servers with missing required exporters or checks
    report_df = pd.DataFrame(columns=['Configuration Item Name', 'Missing Exporters/Checks'])
    
    # Iterate through each configuration item
    for index, config_row in config_df.iterrows():
        server_type = config_row['Configuration Item Name']
        
        if server_type in matrix_df.index:
            # Get all required items (exporters and checks) for this server type from the matrix
            required_exporters_checks = matrix_df.loc[server_type] == 'Y'
            required_exporters_checks = required_exporters_checks[required_exporters_checks].index.tolist()
            
            missing_items = []
            for item in required_exporters_checks:
                # Special handling for boolean fields
                if item in boolean_fields:
                    if not config_row.get(item, False) == 'TRUE':
                        missing_items.append(item)
                else:
                    # Normal handling for exporter fields
                    exporter_field = 'Exporter_name_' + item.split('_')[-1]  # Construct the field name
                    if exporter_field not in config_row or pd.isna(config_row[exporter_field]):
                        missing_items.append(item)
            
            # If there are missing items, add an entry to the report
            if missing_items:
                report_df = report_df.append({
                    'Configuration Item Name': server_type, 
                    'Missing Exporters/Checks': ', '.join(missing_items)
                }, ignore_index=True)

    # Instead of saving the report to a CSV file, return the DataFrame
    return report_df

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         config_file = request.files['file']
#         matrix_file = request.files['existing_yaml']

#         if config_file and matrix_file:
#             report_df = validate_configuration_against_matrix(config_file, matrix_file)
            
#             # Generate a temporary file to store the report
#             temp_file_path = os.path.join(tempfile.gettempdir(), 'validation_report.csv')
#             report_df.to_csv(temp_file_path, index=False)
            
#             return send_file(temp_file_path, as_attachment=True, attachment_filename='validation_report.csv', cache_timeout=0)

#    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
