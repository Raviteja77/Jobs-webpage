from flask import flash, redirect, render_template, request, url_for
from .forms import PostJobForm
from app.models import Job
from . import main
from flask_login import login_required, current_user
from app import db

@main.route("/")
def index():
    category = request.args.get('category', '')
    jobs = Job.query.filter(Job.job_category.ilike(f'%{category}%')).all()
    categories = set([j.job_category.lower() for j in jobs])
    return render_template("home.html", jobs=jobs, user = current_user, category=category.lower(), categories=categories)

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
        user_id = current_user.id
        new_job = Job(job_title = job_title, salary_range = salary_range, company = company, job_category = job_category, job_description = job_description, email = email, closed = closed, user_id = user_id)
        db.session.add(new_job)
        db.session.commit()
        flash('Posted new job successfully!', category='success')
        return redirect(url_for('main.index'))
    postJob = PostJobForm()
    return render_template("create_job.html", form = postJob, user = current_user)

@main.route("/job-detail/<int:id>")
def show_job(id):
    job = Job.query.get(id)
    return render_template("job_details.html", job = job, user = current_user)