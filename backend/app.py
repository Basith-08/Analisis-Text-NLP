from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
from nlp_processor import NLPProcessor
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# --- Artifacts Storage ---
# Global storage for trained models and vectorizers
trained_artifacts = {}

# Paths for model persistence
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_model.joblib')
os.makedirs(MODELS_DIR, exist_ok=True)


def load_model():
    """Load model from disk if it exists"""
    if os.path.exists(MODEL_PATH):
        try:
            artifacts = joblib.load(MODEL_PATH)
            trained_artifacts['best_model'] = artifacts['model']
            trained_artifacts['best_vectorizer'] = artifacts['vectorizer']
            trained_artifacts['label_names'] = artifacts['label_names']
            print(f"✅ Model loaded successfully from {MODEL_PATH}")
            return True
        except Exception as e:
            print(f"⚠️ Error loading model from {MODEL_PATH}: {e}")
            return False
    else:
        print("ℹ️ No pre-trained model found at {MODEL_PATH}. Please train a model via the API or ensure it was saved correctly.")
        return False

# --- Initialization ---
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
        apply_stemming = data.get('apply_stemming', False)  # Get stemming option
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
            processed = nlp_processor.preprocess(original_text, apply_stemming=apply_stemming)

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
        apply_stemming = data.get('apply_stemming', False)  # Get stemming option

        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Text is required'
            }), 400

        # Preprocess
        processed = nlp_processor.preprocess(text, apply_stemming=apply_stemming)

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

@app.route('/api/train_evaluate', methods=['POST'])
def train_evaluate():
    """Train and evaluate models, then save the best one."""
    try:
        data = request.json
        filename = data.get('filename')
        text_column = data.get('text_column')
        label_column = data.get('label_column')
        apply_stemming = data.get('apply_stemming', False)

        if not all([filename, text_column, label_column]):
            return jsonify({
                'status': 'error',
                'message': 'filename, text_column, and label_column are required'
            }), 400

        filepath = os.path.join(DATASETS_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'status': 'error', 'message': 'Dataset not found'}), 404

        df = pd.read_csv(filepath)

        if text_column not in df.columns or label_column not in df.columns:
            return jsonify({'status': 'error', 'message': 'text_column or label_column not found'}), 400
        
        # --- Data Cleaning: Drop rows with missing values in specified columns ---
        df.dropna(subset=[text_column, label_column], inplace=True)

        if df.empty:
            return jsonify({'status': 'error', 'message': f'The dataset is empty after removing rows with missing values in "{text_column}" or "{label_column}".'}), 400

        # --- Data Cleaning: Remove classes with only one member ---
        # This is crucial for preventing errors during stratified splitting.
        label_counts = df[label_column].value_counts()
        labels_to_keep = label_counts[label_counts >= 2].index
        
        original_rows = len(df)
        df = df[df[label_column].isin(labels_to_keep)]
        cleaned_rows = len(df)
        
        if cleaned_rows < original_rows:
            print(f"⚠️ Warning: Removed {original_rows - cleaned_rows} rows with unique or rare labels to prevent training errors.")

        if cleaned_rows < 2:
            return jsonify({'status': 'error', 'message': 'Not enough data left to train after cleaning rare labels.'}), 400

        # Preprocess text data
        df['processed_text'] = df[text_column].apply(
            lambda x: " ".join(nlp_processor.preprocess(str(x), apply_stemming=apply_stemming)['filtered_tokens'])
        )

        X = df['processed_text']
        y = df[label_column].astype(str)
        
        label_names = sorted(y.unique().tolist())
        trained_artifacts['label_names'] = label_names # Store label names

        if len(label_names) < 2:
            return jsonify({'status': 'error', 'message': 'The label column must have at least two unique classes after cleaning.'}), 400


        try:
            # Attempt to stratify the split. This can fail if a class has only one member.
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        except ValueError:
            # If stratification fails, fall back to a regular split and print a warning.
            print("⚠️ Warning: Could not stratify data. Falling back to a non-stratified split. This may be caused by classes with too few members.")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        vectorizers = {'bow': CountVectorizer(), 'tfidf': TfidfVectorizer()}
        X_train_vec = {name: vec.fit_transform(X_train) for name, vec in vectorizers.items()}
        X_test_vec = {name: vec.transform(X_test) for name, vec in vectorizers.items()}

        models = {
            'naive_bayes': MultinomialNB(),
            'decision_tree': DecisionTreeClassifier(random_state=42),
            'svm': SVC(random_state=42, probability=True)
        }
        
        # Temp storage for this request
        trained_models_this_request = {'vectorizers': vectorizers}
        results = {}

        for vec_name in vectorizers:
            results[vec_name] = {}
            for model_name, model in models.items():
                model.fit(X_train_vec[vec_name], y_train)
                y_pred = model.predict(X_test_vec[vec_name])
                
                accuracy = accuracy_score(y_test, y_pred)
                precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
                cm = confusion_matrix(y_test, y_pred)
                
                results[vec_name][model_name] = {
                    'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1_score': f1,
                    'confusion_matrix': cm.tolist()
                }
                trained_models_this_request[f"{vec_name}_{model_name}"] = model

        best_model_name, best_vec_name, best_accuracy = None, None, -1.0
        for vec_name, model_results in results.items():
            for model_name, metrics in model_results.items():
                if metrics['accuracy'] > best_accuracy:
                    best_accuracy = metrics['accuracy']
                    best_model_name = model_name
                    best_vec_name = vec_name
        
        # Update global artifacts with the best model
        best_model_key = f"{best_vec_name}_{best_model_name}"
        trained_artifacts['best_model'] = trained_models_this_request.get(best_model_key)
        trained_artifacts['best_vectorizer'] = trained_models_this_request.get('vectorizers', {}).get(best_vec_name)

        # --- Persist the best model to disk ---
        try:
            model_to_save = {
                'model': trained_artifacts['best_model'],
                'vectorizer': trained_artifacts['best_vectorizer'],
                'label_names': label_names
            }
            joblib.dump(model_to_save, MODEL_PATH)
            print(f"✅ Best model ({best_model_name} with {best_vec_name}) saved to {MODEL_PATH}")
        except Exception as e:
            print(f"⚠️ Error saving model: {e}")

        return jsonify({
            'status': 'success',
            'results': results,
            'best_model_summary': {
                'vectorization': best_vec_name, 'model': best_model_name, 'accuracy': best_accuracy
            },
            'label_names': label_names
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict sentiment for custom text using the best model."""
    try:
        data = request.json
        text = data.get('text')
        apply_stemming = data.get('apply_stemming', False)

        if not text:
            return jsonify({'status': 'error', 'message': 'Text is required'}), 400

        best_model = trained_artifacts.get('best_model')
        best_vectorizer = trained_artifacts.get('best_vectorizer')

        if not best_model or not best_vectorizer:
            return jsonify({
                'status': 'error', 'message': 'Model not trained or loaded. Please train a model first.'
            }), 400

        processed_text = " ".join(nlp_processor.preprocess(text, apply_stemming=apply_stemming)['filtered_tokens'])
        vectorized_text = best_vectorizer.transform([processed_text])
        
        prediction = best_model.predict(vectorized_text)
        prediction_proba = best_model.predict_proba(vectorized_text)

        label_names = trained_artifacts.get('label_names', [])
        if not label_names: # Fallback for safety
             label_names = best_model.classes_

        probabilities = {label: float(prob) for label, prob in zip(label_names, prediction_proba[0])}

        return jsonify({
            'status': 'success',
            'prediction': prediction[0],
            'probabilities': probabilities
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    load_model() # Attempt to load a pre-trained model on startup
    print(f"📂 Datasets folder: {DATASETS_FOLDER}")
    print("✅ Backend is ready and running.")
    app.run(debug=True, host='0.0.0.0', port=5000)
