from flask import Flask, request, render_template, flash, redirect, send_file, url_for,session, Response, render_template_string
from subjective import SubjectiveTest
import nltk
import pdfkit

app = Flask(__name__)

app.secret_key= 'aica2'

# first run these three lines of code
# import nltk
# nltk.download("all")
# exit()

from PyPDF2 import PdfFileReader, PdfReader
from flask import Flask, request

from pdfminer.high_level import extract_text


@app.route('/')
def index():
	return render_template('front.html')

@app.route('/predict')
def index1():
     return render_template('predict.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
    if 'pdf_file' not in request.files:
        return "No file part"

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file"

    if pdf_file:
        pdf = PdfReader(pdf_file)
        text = ""

        for page in pdf.pages:
            text += page.extract_text()

    no_of_questions = 100

    try:
        subjective_generator = SubjectiveTest(text, no_of_questions)
        question_list = subjective_generator.generate_questions()
        return render_template('predict.html', cresults=question_list)

    except:
        flash('Error Occurred!')
        return redirect(url_for('/predict'))

@app.route("/generate")
def gen():
     return render_template('generate.html')

@app.route("/generatepdf", methods=['POST'])

def generate():
    if request.method == "POST":
    
        name = request.form['Name']
        email = request.form['Email']
        linkedin = request.form['LinkedIn']
        experience = request.form['Experience']
        graduation = request.form['Graduation']
        cpga = request.form['CGPA']
        university = request.form['University']
        skills = request.form['Skills']
        internship = request.form['Internship']
        achievements = request.form['Achievements']
        course1 = request.form['course1']
        course2 = request.form['course2']
        course3 = request.form['course3']
        projects = request.form['projects']

        html_content = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
</head>
<body>
    <div class="container">
        <h1 style="font-size: 45px;">{name}</h1>
        <p>Email: {email}</p>
        <p>{linkedin}</p>
        <p>Experience: {experience} years</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Education</h2>
        <p>{graduation} - {university}</p>
        <p>CGPA - {cpga}</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Projects</h2>
        <p>{projects}</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Skills</h2>
        <p>{skills}</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Internships</h2>
        <p>{internship}</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Achievements</h2>
        <p>{achievements}</p>

        <hr style="height: 2px; background-color: #000; border: none; margin-top: 20px; margin-bottom: 20px;">

        <h2>Courses</h2>
        <p>{course1}</p>
        <p>{course2}</p>
        <p>{course3}</p>
    </div>
</body>
</html>

        """

        pdf_path = 'resume.pdf'
        pdfkit.from_string(html_content, pdf_path)
        return render_template('downloadpdf.html', pdf_path=pdf_path)
    return render_template('cantdownload.html')







# Add these imports at the top with other imports
import os
from datetime import datetime

# Add after your existing routes in app.py

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/generateportfolio", methods=['POST'])
def generate_portfolio():
    if request.method == "POST":
        # Personal Information
        name = request.form['Name']
        email = request.form['Email']
        phone = request.form['Phone']
        linkedin = request.form['LinkedIn']
        github = request.form['GitHub']
        location = request.form['Location']
        
        # Professional Information
        title = request.form['Title']
        summary = request.form['Summary']
        skills = request.form['Skills']
        
        # Projects
        projects = []
        i = 1
        while f'project_title_{i}' in request.form:
            if request.form[f'project_title_{i}']:
                projects.append({
                    'title': request.form[f'project_title_{i}'],
                    'description': request.form[f'project_description_{i}'],
                    'technologies': request.form[f'project_technologies_{i}'],
                    'link': request.form[f'project_link_{i}']
                })
            i += 1
        
        # Education
        education = []
        i = 1
        while f'edu_degree_{i}' in request.form:
            if request.form[f'edu_degree_{i}']:
                education.append({
                    'degree': request.form[f'edu_degree_{i}'],
                    'institution': request.form[f'edu_institution_{i}'],
                    'year': request.form[f'edu_year_{i}'],
                    'details': request.form[f'edu_details_{i}']
                })
            i += 1
        
        # Experience
        experience = []
        i = 1
        while f'exp_title_{i}' in request.form:
            if request.form[f'exp_title_{i}']:
                experience.append({
                    'title': request.form[f'exp_title_{i}'],
                    'company': request.form[f'exp_company_{i}'],
                    'duration': request.form[f'exp_duration_{i}'],
                    'description': request.form[f'exp_description_{i}']
                })
            i += 1

        # Generate HTML content for portfolio
        html_content = generate_portfolio_html(name, title, summary, contact_info={
            'email': email,
            'phone': phone,
            'linkedin': linkedin,
            'github': github,
            'location': location
        }, skills=skills, projects=projects, education=education, experience=experience)
        
        pdf_path = f'portfolio_{name.replace(" ", "_")}.pdf'
        pdfkit.from_string(html_content, pdf_path)
        
        return render_template('downloadportfolio.html', pdf_path=pdf_path, name=name)
    
    return render_template('cantdownload.html')

def generate_portfolio_html(name, title, summary, contact_info, skills, projects, education, experience):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name} - Portfolio</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .header {{
                text-align: center;
                padding: 40px 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 3em;
                margin: 0;
                font-weight: 300;
            }}
            .header p {{
                font-size: 1.5em;
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .contact-info {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 20px;
                margin: 20px 0;
            }}
            .contact-info a {{
                color: white;
                text-decoration: none;
            }}
            .section {{
                background: white;
                padding: 30px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .section h2 {{
                color: #667eea;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .skills {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .skill-tag {{
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
            }}
            .project, .education-item, .experience-item {{
                margin-bottom: 25px;
                padding-bottom: 25px;
                border-bottom: 1px solid #eee;
            }}
            .project:last-child, .education-item:last-child, .experience-item:last-child {{
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }}
            .project h3, .education-item h3, .experience-item h3 {{
                color: #333;
                margin-bottom: 5px;
            }}
            .project-link {{
                color: #667eea;
                text-decoration: none;
            }}
            .technologies {{
                font-style: italic;
                color: #666;
                margin: 10px 0;
            }}
            .duration {{
                color: #888;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{name}</h1>
            <p>{title}</p>
            <div class="contact-info">
                <a href="mailto:{contact_info['email']}">📧 {contact_info['email']}</a>
                <a href="tel:{contact_info['phone']}">📱 {contact_info['phone']}</a>
                <a href="{contact_info['linkedin']}">💼 LinkedIn</a>
                <a href="{contact_info['github']}">🐙 GitHub</a>
                <span>📍 {contact_info['location']}</span>
            </div>
        </div>

        <div class="section">
            <h2>Professional Summary</h2>
            <p>{summary}</p>
        </div>

        <div class="section">
            <h2>Skills & Technologies</h2>
            <div class="skills">
                {''.join([f'<span class="skill-tag">{skill.strip()}</span>' for skill in skills.split(',')])}
            </div>
        </div>

        <div class="section">
            <h2>Projects</h2>
            {''.join([f'''
            <div class="project">
                <h3>{project['title']}</h3>
                <p>{project['description']}</p>
                <div class="technologies"><strong>Technologies:</strong> {project['technologies']}</div>
                {f'<a href="{project["link"]}" class="project-link" target="_blank">🔗 View Project</a>' if project['link'] else ''}
            </div>
            ''' for project in projects])}
        </div>

        <div class="section">
            <h2>Experience</h2>
            {''.join([f'''
            <div class="experience-item">
                <h3>{exp['title']}</h3>
                <div class="duration">{exp['company']} | {exp['duration']}</div>
                <p>{exp['description']}</p>
            </div>
            ''' for exp in experience])}
        </div>

        <div class="section">
            <h2>Education</h2>
            {''.join([f'''
            <div class="education-item">
                <h3>{edu['degree']}</h3>
                <div class="duration">{edu['institution']} | {edu['year']}</div>
                <p>{edu['details']}</p>
            </div>
            ''' for edu in education])}
        </div>
    </body>
    </html>
    """



if __name__ == "__main__":
    app.run(debug=True)
