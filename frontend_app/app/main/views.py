import json
import requests
from flask import flash, redirect, render_template, request, url_for
from .forms import PostJobForm
from app.models import Application, Job
from . import main
from flask_login import login_required, current_user
from app import db

SERVER_BASE_URL = "http://localhost:5001/api"

@main.route("/")
def index():
    response = requests.get(SERVER_BASE_URL + "/jobs")
    categories = ["Science and Research", "Manufacturing and Production", "Information Technology", "Human Resources", "Healthcare and Medical", "Education and Training", "Customer Service", "Communications", "Business Development", "Banking and Finance", "Architecture", "Agriculture"]
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    jobs_query = json.loads(response.json())

    if category:
        jobs_query = [job for job in jobs_query if category in job['job_category'].lower()]

    if search:
        jobs_query = [job for job in jobs_query if search.lower() in job['job_title'].lower() or search.lower() in job['job_description'].lower()]
        
    return render_template("home.html", jobs=jobs_query, user=current_user, category=category.lower(), categories=categories)

@main.route("/create-job", methods=["POST", "GET"])
@login_required
def create_job():
    if request.method == 'POST':  
        data = {
            'job_title': request.form.get("job_title"),
            'salary_range': request.form.get("salary_range"),
            'company': request.form.get("company"),
            'job_category': request.form.get("job_category"),
            'job_description': request.form.get("job_description"),
            'email': current_user.email,
            'closed': False
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(SERVER_BASE_URL + "/jobs", data=json.dumps(data), headers=headers)

        decoded_response = response.json()

        flash(decoded_response['message'], category=decoded_response['status'])
        return redirect(url_for('main.index'))
    postJob = PostJobForm()
    return render_template("create_job.html", form = postJob, user = current_user)

@main.route("/job-detail/<int:id>")
@login_required
def show_job(id):
    response = requests.get(f"http://localhost:5001/api/job/{id}")
    job = json.loads(response.json())
    return render_template("job_details.html", job = job, user = current_user)

@main.route("/close-job/<int:id>")
@login_required
def close_job(id):
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"http://localhost:5001/api/job/{id}", headers=headers)
    decoded_response = response.json()

    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')

@main.route("/applicant-applied-jobs/<int:id>")
@login_required
def applicant_jobs(id):
    headers = {'Content-Type': 'application/json'}
    user = {
        'id': current_user.id
    }

    response = requests.post(f"http://localhost:5001/api/job/{id}", data=json.dumps(user), headers=headers)
    decoded_response = response.json()
    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')

# @main.route("/applied-jobs")
# @login_required
# def applied_jobs():
#     user_id = current_user.id
#     applications = Application.query.filter_by(user_id=user_id).all()
#     jobs = [application.job for application in applications]
#     return render_template("applied_jobs.html", user=current_user, applications=applications, jobs = jobs)

# @main.route("/applicants-list")
# @login_required
# def applicants():
#     applications = Application.query.all()
#     jobs = [application.job for application in applications if application.job.email == current_user.email]
#     applications = [application for application in applications if application.job.email == current_user.email]
#     print(len(jobs))
#     return render_template("job_applicants.html", user=current_user, applications=applications, jobs = jobs)