from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app)

# Load AI models (assuming these exist)
try:
    vectorizer = joblib.load('vectorizer.joblib')
    le = joblib.load('label_encoder.joblib')
    clf = joblib.load('task_classifier.joblib')
    models_loaded = True
except:
    models_loaded = False
    print("Warning: AI models not found. Category prediction will be disabled.")

# Use a CSV file as a simple database
TASKS_FILE = 'tasks.csv'
if not os.path.exists(TASKS_FILE):
    pd.DataFrame(columns=[
        'id', 'title', 'description', 'category', 'status', 
        'priority', 'deadline', 'created_at', 'completed_at'
    ]).to_csv(TASKS_FILE, index=False)

def load_tasks():
    df = pd.read_csv(TASKS_FILE)
    # Convert NaN to None for JSON serialization
    return df.where(pd.notnull(df), None)

def save_tasks(df):
    df.to_csv(TASKS_FILE, index=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    df = load_tasks()
    
    # Query parameters for filtering
    status = request.args.get('status')
    priority = request.args.get('priority')
    category = request.args.get('category')
    search = request.args.get('search')
    overdue = request.args.get('overdue')
    due_soon = request.args.get('due_soon')
    
    # Apply filters
    if status and status != 'all':
        df = df[df['status'] == status]
    
    if priority and priority != 'all':
        df = df[df['priority'] == priority]
    
    if category and category != 'all':
        df = df[df['category'] == category]
    
    if search:
        search_mask = (
            df['title'].str.contains(search, case=False, na=False) |
            df['description'].str.contains(search, case=False, na=False)
        )
        df = df[search_mask]
    
    if overdue == 'true':
        today = datetime.now().date()
        df['deadline_date'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
        df = df[(df['deadline_date'] < today) & (df['status'] != 'completed')]
        df = df.drop('deadline_date', axis=1)
    
    if due_soon == 'true':
        today = datetime.now().date()
        three_days = today + timedelta(days=3)
        df['deadline_date'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
        df = df[
            (df['deadline_date'] >= today) & 
            (df['deadline_date'] <= three_days) & 
            (df['status'] != 'completed')
        ]
        df = df.drop('deadline_date', axis=1)
    
    # Ensure output is always a list, not a dict
    tasks = df.where(pd.notnull(df), None).to_dict(orient='records')
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    df = load_tasks()
    
    # Generate new ID
    new_id = int(df['id'].max()) + 1 if not df.empty and not df['id'].isna().all() else 1
    
    # Add metadata
    data['id'] = new_id
    data['created_at'] = datetime.now().isoformat()
    data['completed_at'] = None
    
    # Validate required fields
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    # Set defaults
    data.setdefault('status', 'todo')
    data.setdefault('priority', 'medium')
    data.setdefault('category', '')
    
    # Add to dataframe
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    save_tasks(df)
    
    return jsonify({'message': 'Task created successfully', 'id': new_id, 'task': data})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    df = load_tasks()
    
    # Find task
    task_idx = df.index[df['id'] == task_id]
    if task_idx.empty:
        return jsonify({'error': 'Task not found'}), 404
    
    idx = task_idx[0]
    
    # Update completion timestamp
    if data.get('status') == 'completed' and df.at[idx, 'status'] != 'completed':
        data['completed_at'] = datetime.now().isoformat()
    elif data.get('status') != 'completed':
        data['completed_at'] = None
    
    # Update fields
    for key, value in data.items():
        if key in df.columns:
            df.at[idx, key] = value
    
    save_tasks(df)
    
    updated_task = df.iloc[idx].to_dict()
    return jsonify({'message': 'Task updated successfully', 'task': updated_task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    df = load_tasks()
    
    # Check if task exists
    if task_id not in df['id'].values:
        return jsonify({'error': 'Task not found'}), 404
    
    # Remove task
    df = df[df['id'] != task_id]
    save_tasks(df)
    
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/tasks/bulk', methods=['POST'])
def bulk_operations():
    data = request.json
    operation = data.get('operation')
    task_ids = data.get('task_ids', [])
    
    if not operation or not task_ids:
        return jsonify({'error': 'Operation and task_ids are required'}), 400
    
    df = load_tasks()
    
    if operation == 'delete':
        df = df[~df['id'].isin(task_ids)]
        save_tasks(df)
        return jsonify({'message': f'Deleted {len(task_ids)} tasks'})
    
    elif operation == 'update_status':
        new_status = data.get('status')
        if not new_status:
            return jsonify({'error': 'Status is required for update operation'}), 400
        
        mask = df['id'].isin(task_ids)
        df.loc[mask, 'status'] = new_status
        
        # Update completion timestamps
        if new_status == 'completed':
            df.loc[mask, 'completed_at'] = datetime.now().isoformat()
        else:
            df.loc[mask, 'completed_at'] = None
        
        save_tasks(df)
        return jsonify({'message': f'Updated {len(task_ids)} tasks'})
    
    return jsonify({'error': 'Invalid operation'}), 400

@app.route('/predict_category', methods=['POST'])
def predict_category():
    if not models_loaded:
        # Fallback categories when models are not available
        fallback_categories = ['Work', 'Personal', 'Shopping', 'Health', 'Education', 'Finance']
        import random
        return jsonify({'predicted_category': random.choice(fallback_categories)})
    
    data = request.json
    text = data.get('title', '') + ' ' + data.get('description', '')
    
    if not text.strip():
        return jsonify({'error': 'Title or description is required'}), 400
    
    try:
        X = vectorizer.transform([text])
        pred = clf.predict(X)
        category = le.inverse_transform(pred)[0]
        
        # Get prediction confidence
        probabilities = clf.predict_proba(X)[0]
        confidence = float(np.max(probabilities))
        
        return jsonify({
            'predicted_category': category,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    df = load_tasks()
    
    if df.empty:
        return jsonify({
            'total_tasks': 0,
            'completed_tasks': 0,
            'in_progress_tasks': 0,
            'overdue_tasks': 0,
            'due_soon_tasks': 0,
            'completion_rate': 0,
            'category_distribution': {},
            'priority_distribution': {},
            'status_distribution': {}
        })
    
    total_tasks = len(df)
    completed_tasks = len(df[df['status'] == 'completed'])
    in_progress_tasks = len(df[df['status'] == 'in_progress'])
    
    # Calculate overdue and due soon tasks
    today = datetime.now().date()
    three_days = today + timedelta(days=3)
    
    df['deadline_date'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
    overdue_tasks = len(df[
        (df['deadline_date'] < today) & 
        (df['status'] != 'completed') & 
        df['deadline_date'].notna()
    ])
    
    due_soon_tasks = len(df[
        (df['deadline_date'] >= today) & 
        (df['deadline_date'] <= three_days) & 
        (df['status'] != 'completed') & 
        df['deadline_date'].notna()
    ])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Distribution stats
    category_dist = df['category'].value_counts().to_dict()
    priority_dist = df['priority'].value_counts().to_dict()
    status_dist = df['status'].value_counts().to_dict()
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'due_soon_tasks': due_soon_tasks,
        'completion_rate': round(completion_rate, 2),
        'category_distribution': category_dist,
        'priority_distribution': priority_dist,
        'status_distribution': status_dist
    })

@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400
    
    df = load_tasks()
    
    # Search in title, description, and category
    search_mask = (
        df['title'].str.contains(query, case=False, na=False) |
        df['description'].str.contains(query, case=False, na=False) |
        df['category'].str.contains(query, case=False, na=False)
    )
    
    results = df[search_mask]
    return jsonify(results.to_dict(orient='records'))

@app.route('/categories', methods=['GET'])
def get_categories():
    df = load_tasks()
    categories = df['category'].dropna().unique().tolist()
    return jsonify(categories)

@app.route('/export', methods=['GET'])
def export_tasks():
    df = load_tasks()
    format_type = request.args.get('format', 'csv')
    
    if format_type == 'json':
        return jsonify(df.to_dict(orient='records'))
    else:
        # Return CSV data
        csv_data = df.to_csv(index=False)
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=tasks.csv'
        }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': models_loaded
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'AI Task Management System Backend',
        'version': '2.0',
        'endpoints': [
            '/tasks - GET, POST',
            '/tasks/<id> - PUT, DELETE',
            '/tasks/bulk - POST',
            '/predict_category - POST',
            '/stats - GET',
            '/search - GET',
            '/categories - GET',
            '/export - GET',
            '/health - GET'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)