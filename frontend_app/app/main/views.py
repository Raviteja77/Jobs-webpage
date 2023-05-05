import json
import requests
from flask import flash, redirect, render_template, request, url_for
from .forms import PostJobForm
from . import main
from flask_login import login_required, current_user

# Define the base URL for the server API
SERVER_BASE_URL = "http://localhost:5001/api/"

# Define the route for the main page of the website
@main.route("/")
def index():
    # Send a GET request to the server to retrieve the list of jobs
    jobs_response = requests.get(SERVER_BASE_URL + "jobs")

    # Define a list of job categories for filtering purposes
    categories = ["Science and Research", "Manufacturing and Production", "Information Technology", "Human Resources", "Healthcare and Medical", "Education and Training", "Customer Service", "Communications", "Business Development", "Banking and Finance", "Architecture", "Agriculture"]

    # Retrieve the 'category' and 'search' query parameters from the request
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    applied_jobs = None
    # Send a GET request to the server to retrieve the list of applications for the current user
    if(current_user.is_authenticated and current_user.role == 'applicant'):
        id = current_user.id
        applications_response = requests.get(f"{SERVER_BASE_URL}application/{id}")
        applications_query = json.loads(applications_response.json())

        # Extract the job IDs from the applications list for use in the template
        applied_jobs = [d['job_id'] for d in applications_query]

    # Parse the list of jobs returned by the server
    jobs_query = json.loads(jobs_response.json())

    # If a category query parameter was provided, filter the list of jobs accordingly
    if category:
        jobs_query = [job for job in jobs_query if category in job['job_category'].lower()]

    # If a search query parameter was provided, filter the list of jobs accordingly
    if search:
        jobs_query = [job for job in jobs_query if search.lower() in job['job_title'].lower() or search.lower() in job['job_description'].lower()]
        
    # Render the template with the filtered list of jobs and other information
    return render_template("home.html", jobs=jobs_query, applications=applied_jobs, user=current_user, category=category.lower(), categories=categories)

# Define the route for creating a new job listing
@main.route("/create-job", methods=["POST", "GET"])
@login_required
def create_job():
    # If the request method is POST, process the form data and submit a new job listing to the server
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
        response = requests.post(SERVER_BASE_URL + "jobs", data=json.dumps(data), headers=headers)

        decoded_response = response.json()

        # Display a flash message indicating whether the job listing was successfully submitted
        flash(decoded_response['message'], category=decoded_response['status'])
        return redirect(url_for('main.index'))

    # If the request method is GET, display the job creation form
    postJob = PostJobForm()
    return render_template("create_job.html", form = postJob, user = current_user)

# Define the route for viewing the details of a specific job listing
@main.route("/job-detail/<int:id>")
@login_required
def show_job(id):
    # Send a GET request to the server to retrieve the details of the specified job listing
    job_response = requests.get(f"{SERVER_BASE_URL}job/{id}")
    job = json.loads(job_response.json())
    # create a dictionary with the current user's email
    data = {
        'email': current_user.email
    }
    headers = {'Content-Type': 'application/json'}
    # get the list of applicants for the job by making a GET request to the API with the user's email
    applicants_response = requests.get(f"{SERVER_BASE_URL}applicants", data=json.dumps(data), headers=headers)
    job_applicants = json.loads(applicants_response.json())
    # render the job details page with the job and list of applicants for the job
    return render_template("job_details.html", job=job, applicants=job_applicants, user=current_user)

@main.route("/close-job/<int:id>")
@login_required
def close_job(id):
    # create a dictionary with the 'closed' key set to True to update the job status
    data = {
        'closed': True
    }
    headers = {'Content-Type': 'application/json'}
    # update the job status by making a PUT request to the API with the job id and the updated data
    response = requests.put(f"{SERVER_BASE_URL}job/{id}", data=json.dumps(data), headers=headers)
    decoded_response = response.json()
    # display a message to the user indicating whether the job was closed successfully or not
    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')

@main.route("/applicant-withdraw-job/<int:id>")
@login_required
def withdraw_job(id):
    headers = {'Content-Type': 'application/json'}
    # remove the application for the job by making a DELETE request to the API with the application id
    response = requests.delete(f"{SERVER_BASE_URL}application/{id}", headers=headers)
    decoded_response = response.json()
    # display a message to the user indicating whether the application was withdrawn successfully or not
    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')

@main.route("/applicant-applied-jobs/<int:id>")
@login_required
def applicant_jobs(id):
    headers = {'Content-Type': 'application/json'}
    # create a dictionary with the current user's id to get a list of all jobs the user has applied for
    user = {
        'id': current_user.id
    }
    # make a POST request to the API with the user id to get the list of jobs the user has applied for
    response = requests.post(f"{SERVER_BASE_URL}job/{id}", data=json.dumps(user), headers=headers)
    decoded_response = response.json()
    # display a message to the user indicating whether the request was successful or not
    flash(decoded_response['message'], category=decoded_response['status'])
    return redirect('/')
