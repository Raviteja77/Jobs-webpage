from flask import flash, redirect, render_template, request, url_for
from .forms import PostJobForm
from app.models import Application, Job, User
from . import main
from flask_login import login_required, current_user
from app import db

@main.route("/")
def index():
    categories = ["Science and Research", "Manufacturing and Production", "Information Technology", "Human Resources", "Healthcare and Medical", "Education and Training", "Customer Service", "Communications", "Business Development", "Banking and Finance", "Architecture", "Agriculture"]
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    jobs_query = Job.query.filter(Job.closed == False)

    if category:
        jobs_query = jobs_query.filter(Job.job_category.ilike(f'%{category}%'))

    if search:
        jobs_query = jobs_query.filter((Job.job_title.ilike(f'%{search}%') | Job.job_description.ilike(f'%{search}%')))

    jobs = jobs_query.all()

    return render_template("home.html", jobs=jobs, user=current_user, category=category.lower(), categories=categories)

@main.route("/create-job", methods=["POST", "GET"])
@login_required
def create_job():
    if request.method == 'POST':
        job_title = request.form.get("job_title")
        salary_range = request.form.get("salary_range")
        company = request.form.get("company")
        job_category = request.form.get("job_category")
        job_description = request.form.get("job_description")
        email = current_user.email
        closed = False
        new_job = Job(job_title = job_title, salary_range = salary_range, company = company, job_category = job_category, job_description = job_description, email = email, closed = closed)
        db.session.add(new_job)
        db.session.commit()
        flash('Posted new job successfully!', category='success')
        return redirect(url_for('main.index'))
    postJob = PostJobForm()
    return render_template("create_job.html", form = postJob, user = current_user)

@main.route("/job-detail/<int:id>")
@login_required
def show_job(id):
    job = Job.query.get(id)
    return render_template("job_details.html", job = job, user = current_user)

@main.route("/close-job/<int:id>")
@login_required
def close_job(id):
    job = Job.query.get(id)
    job.closed = True
    db.session.add(job)
    db.session.commit()
    flash('Job closed successfully', category='success')
    return redirect('/')

@main.route("/applied-jobs")
@login_required
def applied_jobs():
    user_id = current_user.id
    applications = Application.query.filter_by(user_id=user_id).all()
    jobs = [application.job for application in applications]
    return render_template("applied_jobs.html", user=current_user, applications=applications, jobs = jobs)

@main.route("/applicant-applied-jobs/<int:id>")
@login_required
def applicant_jobs(id):
    job = Job.query.get(id)
    user = current_user
    application = Application(user=user, job=job)
    db.session.add(application)
    db.session.commit()
    flash('User successfully applied for the job', category='success')
    return redirect('/')

@main.route("/applicants-list")
@login_required
def applicants():
    applications = Application.query.all()
    jobs = [application.job for application in applications if application.job.email == current_user.email]
    applications = [application for application in applications if application.job.email == current_user.email]
    print(len(jobs))
    return render_template("job_applicants.html", user=current_user, applications=applications, jobs = jobs)