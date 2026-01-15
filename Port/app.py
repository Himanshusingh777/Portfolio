# app.py - Complete Flask Portfolio Application
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Store contact messages (in production, use a database)
MESSAGES_FILE = 'messages.json'

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_message(message_data):
    messages = load_messages()
    message_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    messages.append(message_data)
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

# Projects data
PROJECTS = [
    {
        'id': 1,
        'title': 'SwasthaAI-Agent',
        'description': 'An AI-driven healthcare assistant that performs symptom checking, provides suggestions, and verifies medicines using OCR technology.',
        'tech_stack': ['Python', 'Flask', 'OpenAI API', 'OCR', 'TensorFlow'],
        'category': 'AI/ML',
        'github': 'https://github.com/yourusername/swastha-ai',
        'demo': '#',
        'image': 'swastha.jpg',
        'highlights': [
            'Real-time symptom analysis',
            'Medicine verification using OCR',
            'Intelligent health recommendations',
            'User-friendly interface'
        ]
    },
    {
        'id': 2,
        'title': 'NeuroShield AI',
        'description': 'An AI firewall detecting mental manipulation and cognitive intrusion in real-time communication. Winner of National Hackathon 2024.',
        'tech_stack': ['Python', 'NLP', 'Deep Learning', 'Real-time Analytics'],
        'category': 'AI/ML',
        'github': 'https://github.com/yourusername/neuroshield',
        'demo': '#',
        'image': 'neuroshield.jpg',
        'highlights': [
            'Real-time threat detection',
            'Advanced NLP algorithms',
            'Hackathon Winner',
            '95% accuracy rate'
        ]
    },
    {
        'id': 3,
        'title': 'Campus Placement Analytics',
        'description': 'Comprehensive analytics dashboard analyzing placement trends and student performance metrics for data-driven insights.',
        'tech_stack': ['Python', 'Pandas', 'Power BI', 'Excel', 'Matplotlib'],
        'category': 'Data Analytics',
        'github': 'https://github.com/yourusername/placement-analytics',
        'demo': '#',
        'image': 'placement.jpg',
        'highlights': [
            'Interactive Power BI dashboards',
            'Predictive analytics',
            'Trend analysis',
            'Performance metrics tracking'
        ]
    },
    {
        'id': 4,
        'title': 'Sales Performance Dashboard',
        'description': 'Real-time sales analytics dashboard providing insights into revenue, customer behavior, and market trends.',
        'tech_stack': ['Python', 'Looker Studio', 'SQL', 'Pandas'],
        'category': 'Data Analytics',
        'github': 'https://github.com/yourusername/sales-dashboard',
        'demo': '#',
        'image': 'sales.jpg',
        'highlights': [
            'Real-time data visualization',
            'KPI tracking',
            'Customer segmentation',
            'Revenue forecasting'
        ]
    },
    {
        'id': 5,
        'title': 'Automated Report Generator',
        'description': 'Python-based automation tool that generates comprehensive business reports from raw data sources.',
        'tech_stack': ['Python', 'Pandas', 'Matplotlib', 'FPDF', 'Automation'],
        'category': 'Automation',
        'github': 'https://github.com/yourusername/report-generator',
        'demo': '#',
        'image': 'automation.jpg',
        'highlights': [
            'Automated data processing',
            'PDF report generation',
            'Scheduled reporting',
            'Custom templates'
        ]
    }
]

# Skills data
SKILLS = {
    'Programming': ['Python', 'SQL', 'JavaScript', 'HTML/CSS'],
    'Data Analysis': ['Pandas', 'NumPy', 'Excel', 'Statistical Analysis'],
    'Visualization': ['Power BI', 'Looker Studio', 'Matplotlib', 'Seaborn', 'Plotly'],
    'AI/ML': ['TensorFlow', 'Scikit-learn', 'NLP', 'OpenAI API'],
    'Web Development': ['Flask', 'Django', 'REST APIs', 'Bootstrap'],
    'Tools': ['Git', 'Jupyter', 'VS Code', 'Tableau']
}

# Experience data
EXPERIENCE = [
    {
        'title': 'Research Analyst',
        'company': '3N Performance Partners',
        'duration': '2024 - Present',
        'location': 'Hyderabad, India',
        'responsibilities': [
            'Conducting market research and competitive analysis',
            'Building predictive models for business forecasting',
            'Creating interactive dashboards using Power BI and Looker Studio',
            'Automating data processing workflows',
            'Presenting insights to stakeholders'
        ]
    },
    {
        'title': 'Data Analytics Intern',
        'company': 'Tech Solutions Pvt Ltd',
        'duration': '2023 - 2024',
        'location': 'Remote',
        'responsibilities': [
            'Analyzed customer data to identify trends and patterns',
            'Developed Python scripts for data cleaning and transformation',
            'Created visualization reports using Matplotlib and Seaborn',
            'Collaborated with cross-functional teams'
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', skills=SKILLS, experience=EXPERIENCE)

@app.route('/projects')
def projects():
    category = request.args.get('category', 'all')
    if category != 'all':
        filtered_projects = [p for p in PROJECTS if p['category'] == category]
    else:
        filtered_projects = PROJECTS
    return render_template('projects.html', projects=filtered_projects, selected_category=category)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if project:
        return render_template('project_detail.html', project=project)
    return redirect(url_for('projects'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        message_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'subject': data.get('subject'),
            'message': data.get('message')
        }
        save_message(message_data)
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """API endpoint for portfolio statistics"""
    stats = {
        'projects_completed': len(PROJECTS),
        'skills_mastered': sum(len(v) for v in SKILLS.values()),
        'years_experience': 2,
        'certifications': 5
    }
    return jsonify(stats)
@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)