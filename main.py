from flask import Flask, render_template, request, url_for, redirect
import data_manager
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mentors')
def mentors_list():
    mentor_name = request.args.get('mentor-last-name')
    city_name=request.args.get("city-name")
    if mentor_name:
        mentor_details = data_manager.get_mentors_by_last_name(mentor_name)
    elif city_name:
        mentor_details=data_manager.get_mentors_by_city(city_name)
    else:
        mentor_details = data_manager.get_mentors()
    # We get back a list of dictionaries from the data_manager (for details check 'data_manager.py')
    return render_template('mentors.html', mentors=mentor_details)

@app.route('/applicants-phone')
def applicant_name():
    applicant_n = request.args.get('applicant-name')
    applicant_e =request.args.get('email_ending')
    if applicant_n:
        applicant=data_manager.get_applicant_data_by_name(applicant_n)
    elif applicant_e:
        applicant=data_manager.get_applicant_data_by_email_ending(applicant_e)
    else:
        applicant=''
    return render_template('applicant_phone.html',applicant=applicant)

@app.route('/applicants')
def applicants_list():
    applicants_list=data_manager.get_applicants()
    return render_template('applicants_list.html', applicants_list=applicants_list)

@app.route('/applicants/<application_code>', methods=['GET','POST'])
def applicant_details(application_code):
    applicant=data_manager.show_applicant(application_code)
    if request.method == 'POST':
        update_phone=request.form['new_phone']
        data_manager.update_phone(update_phone,application_code)
        return redirect(request.referrer)
    return render_template('applicant_details.html',applicant=applicant)

@app.route('/applicants/<application_code>/delete')
def delete_applicant(application_code):
    del_applicant=data_manager.delete_applicant(application_code)
    return redirect(request.referrer)
    return render_template('applicants_list.html')

@app.route('/applicants/delete_by_mail', methods=["POST"])
def delete_applicant_by_mail():
    if request.method=="POST":
        del_by_end_mail=request.form['email-ending']
        delete_app=data_manager.delete_by_mail(del_by_end_mail)
        return redirect(request.referrer)
    return render_template('applicants_list.html')

@app.route('/add-applicant', methods=['POST'])
def add_applicant():
    if request.method=="POST":
        first_name= request.form['first_name']
        last_name=request.form['last_name']
        phone_number=request.form['phone_number']
        e_mail=request.form['e_mail']
        application_code= data_manager.generate_code()
        new_applicant=data_manager.add_applicant(first_name,last_name,phone_number,e_mail,application_code)
        return redirect(request.referrer)
    return render_template('applicants_list.html')

if __name__ == '__main__':
    app.run(debug=True)
