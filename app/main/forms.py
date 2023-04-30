from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    role = SelectField("Role", choices=[('role', 'Select a role'), 
                                        ('applicant', 'Applicant'), 
                                        ('manager', 'Hiring Manager')], 
                                        validators=[DataRequired()])
    submit = SubmitField("Submit!")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login!")

class PostJobForm(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired()])
    salary_range = StringField("Salary Range", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    job_category = SelectField("Job Category", choices=[('categories', 'All Categories'), 
                                                        ('Science and Research', 'Science and Research'), 
                                                        ('Manufacturing and Production', 'Manufacturing and Production'), 
                                                        ('Information Technology', 'Information Technology'), 
                                                        ('Human Resources', 'Human Resources'), 
                                                        ('Healthcare and Medical', 'Healthcare and Medical'), 
                                                        ('Education and Training', 'Education and Training'), 
                                                        ('Customer Service', 'Customer Service'), 
                                                        ('Communications', 'Communications'), 
                                                        ('Business Development', 'Business Development'), 
                                                        ('Banking and Finance', 'Banking and Finance'), 
                                                        ('Architecture', 'Architecture'), 
                                                        ('Agriculture', 'Agriculture')], 
                                                        validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField("Post Job!")
    