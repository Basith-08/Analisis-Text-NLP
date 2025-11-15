from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
from nlp_processor import NLPProcessor

app = Flask(__name__)
CORS(app)

# Initialize NLP Processor
nlp_processor = NLPProcessor()

# Path to datasets folder
DATASETS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets')

# Upload configuration
ALLOWED_EXTENSIONS = {'csv'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend is running'
    })

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Get list of available datasets"""
    try:
        if not os.path.exists(DATASETS_FOLDER):
            return jsonify({
                'status': 'error',
                'message': 'Datasets folder not found'
            }), 404

        files = [f for f in os.listdir(DATASETS_FOLDER) if f.endswith('.csv')]
        return jsonify({
            'status': 'success',
            'datasets': files
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/load-dataset', methods=['POST'])
def load_dataset():
    """Load and preview dataset"""
    try:
        data = request.json
        filename = data.get('filename')

        if not filename:
            return jsonify({
                'status': 'error',
                'message': 'Filename is required'
            }), 400

        filepath = os.path.join(DATASETS_FOLDER, filename)

        if not os.path.exists(filepath):
            return jsonify({
                'status': 'error',
                'message': 'Dataset not found'
            }), 404

        # Read CSV
        df = pd.read_csv(filepath)

        # Get columns and preview
        columns = df.columns.tolist()
        preview = df.head(10).to_dict('records')
        total_rows = len(df)

        return jsonify({
            'status': 'success',
            'columns': columns,
            'preview': preview,
            'total_rows': total_rows
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading dataset: {str(e)}'
        }), 500

@app.route('/api/preprocess', methods=['POST'])
def preprocess_text():
    """Preprocess text data from dataset"""
    try:
        data = request.json
        filename = data.get('filename')
        text_column = data.get('text_column')
        limit = data.get('limit', 50)  # Limit results for performance

        if not filename or not text_column:
            return jsonify({
                'status': 'error',
                'message': 'Filename and text_column are required'
            }), 400

        filepath = os.path.join(DATASETS_FOLDER, filename)

        if not os.path.exists(filepath):
            return jsonify({
                'status': 'error',
                'message': 'Dataset not found'
            }), 404

        # Read CSV
        df = pd.read_csv(filepath)

        if text_column not in df.columns:
            return jsonify({
                'status': 'error',
                'message': f'Column "{text_column}" not found in dataset'
            }), 400

        # Limit rows for performance
        df_limited = df.head(limit)

        # Process each text
        results = []
        for idx, row in df_limited.iterrows():
            original_text = str(row[text_column])

            # Preprocess
            processed = nlp_processor.preprocess(original_text)

            results.append({
                'id': int(idx) + 1,
                'original': original_text,
                'cleaned': processed['cleaned'],
                'tokens': processed['tokens'],
                'filtered_tokens': processed['filtered_tokens'],
                'token_count': len(processed['tokens']),
                'filtered_count': len(processed['filtered_tokens'])
            })

        return jsonify({
            'status': 'success',
            'total_processed': len(results),
            'results': results
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error preprocessing: {str(e)}'
        }), 500

@app.route('/api/preprocess-custom', methods=['POST'])
def preprocess_custom_text():
    """Preprocess custom text input"""
    try:
        data = request.json
        text = data.get('text')

        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Text is required'
            }), 400

        # Preprocess
        processed = nlp_processor.preprocess(text)

        return jsonify({
            'status': 'success',
            'original': text,
            'cleaned': processed['cleaned'],
            'tokens': processed['tokens'],
            'filtered_tokens': processed['filtered_tokens'],
            'token_count': len(processed['tokens']),
            'filtered_count': len(processed['filtered_tokens'])
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error preprocessing: {str(e)}'
        }), 500

@app.route('/api/upload-dataset', methods=['POST'])
def upload_dataset():
    """Upload new dataset file"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400

        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Only CSV files are allowed'
            }), 400

        # Secure filename
        filename = secure_filename(file.filename)

        # Ensure datasets folder exists
        if not os.path.exists(DATASETS_FOLDER):
            os.makedirs(DATASETS_FOLDER)

        # Save file
        filepath = os.path.join(DATASETS_FOLDER, filename)
        file.save(filepath)

        # Validate CSV by trying to read it
        try:
            df = pd.read_csv(filepath)
            columns = df.columns.tolist()
            total_rows = len(df)
            preview = df.head(5).to_dict('records')

            return jsonify({
                'status': 'success',
                'message': f'File "{filename}" uploaded successfully',
                'filename': filename,
                'columns': columns,
                'total_rows': total_rows,
                'preview': preview
            })

        except Exception as e:
            # Remove invalid file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'status': 'error',
                'message': f'Invalid CSV file: {str(e)}'
            }), 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error uploading file: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Datasets folder: {DATASETS_FOLDER}")
    app.run(debug=True, host='0.0.0.0', port=5000)
