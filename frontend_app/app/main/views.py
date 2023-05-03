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
    jobs_response = requests.get(SERVER_BASE_URL + "/jobs")
    categories = ["Science and Research", "Manufacturing and Production", "Information Technology", "Human Resources", "Healthcare and Medical", "Education and Training", "Customer Service", "Communications", "Business Development", "Banking and Finance", "Architecture", "Agriculture"]
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    id = current_user.id
    applications_response = requests.get(f"http://localhost:5001/api/application/{id}")
    applications_query = json.loads(applications_response.json())
    applied_jobs = [d['job_id'] for d in applications_query]

    jobs_query = json.loads(jobs_response.json())

    if category:
        jobs_query = [job for job in jobs_query if category in job['job_category'].lower()]

    if search:
        jobs_query = [job for job in jobs_query if search.lower() in job['job_title'].lower() or search.lower() in job['job_description'].lower()]
        
    return render_template("home.html", jobs=jobs_query, applications=applied_jobs, user=current_user, category=category.lower(), categories=categories)

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
    job_response = requests.get(f"http://localhost:5001/api/job/{id}")
    job = json.loads(job_response.json())
    data = {
        'email': current_user.email
    }
    headers = {'Content-Type': 'application/json'}
    applicants_response = requests.get(f"http://localhost:5001/api/applicants", data=json.dumps(data), headers=headers)
    job_applicants = json.loads(applicants_response.json())
    return render_template("job_details.html", job = job, applicants = job_applicants, user = current_user)

@main.route("/close-job/<int:id>")
@login_required
def close_job(id):
    data = {
        'closed': True
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"http://localhost:5001/api/job/{id}", data=json.dumps(data), headers=headers)
    decoded_response = response.json()

    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')

@main.route("/applicant-withdraw-job/<int:id>")
@login_required
def withdraw_job(id):
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f"http://localhost:5001/api/application/{id}", headers=headers)
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