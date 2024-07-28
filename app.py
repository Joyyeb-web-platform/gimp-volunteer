import asyncio
from flask import Flask, render_template, request, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os
from app_logic.send_notification_gimp import send_admin_notification, send_client_notification

app = Flask(__name__)

notification_client = os.environ.get("NOTIFICATION_CLIENT_ID")
notification_secret = os.environ.get("NOTIFICATION_CLIENT_SECRETE")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_volunteer_form', methods=['POST'])
def submit_form():
    full_name = request.form['full_name']
    email = request.form['email']
    mobile_number = request.form['mobile_number']
    school = request.form['school']
    place_of_residence = request.form['place_of_residence']
    level = request.form['level']
    fields_of_coordination = request.form.getlist('fields_of_coordination')
    teams_to_join = request.form.getlist('teams_to_join')
    resume = request.files['resume']

    # Save the resume to a temporary file
    resume_path = os.path.join("static", resume.filename)
    resume.save(resume_path)

    # Generate PDF for volunteer data using ReportLab
    volunteer_data_pdf_path = os.path.join("static", f"{full_name}_volunteer_data.pdf")
    create_volunteer_pdf(volunteer_data_pdf_path, full_name, email, mobile_number, school, place_of_residence, level,
                         fields_of_coordination, teams_to_join)

    # Generate a link to the PDF file
    volunteer_data_link = url_for('static', filename=f"{full_name}_volunteer_data.pdf", _external=True)

    # Generate a link to the resume file
    resume_link = url_for('static', filename=resume.filename, _external=True)

    # Send notification
    asyncio.run(send_admin_notification(notification_client=notification_client,
                                        notification_secret=notification_secret,
                                        volunteer_data_link=volunteer_data_link,
                                        volunteer_resume_link=resume_link))
    asyncio.run(
        send_client_notification(notification_client=notification_client, notification_secret=notification_secret,
                                 volunteer_name=full_name, volunteer_email=email))

    return redirect(url_for('success', name=full_name))


def create_volunteer_pdf(filepath, full_name, email, mobile_number, school, place_of_residence, level,
                         fields_of_coordination, teams_to_join):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = styles['Title']
    title_style.textColor = colors.darkblue
    elements.append(Paragraph("Volunteer Information", title_style))
    elements.append(Spacer(1, 12))

    # Summary Section
    summary_data = [
        ['Full Name:', full_name],
        ['Email:', email],
        ['Mobile Number:', mobile_number],
        ['School:', school],
        ['Place of Residence:', place_of_residence],
        ['Level:', level]
    ]
    summary_table = Table(summary_data, hAlign='LEFT')
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # Detailed Breakdown
    elements.append(Paragraph("Fields of Coordination and Teams to Join", styles['Heading2']))
    elements.append(Spacer(1, 12))
    details_data = [
        ['Fields of Coordination', ', '.join(fields_of_coordination)],
        ['Teams to Join', ', '.join(teams_to_join)]
    ]
    details_table = Table(details_data, hAlign='LEFT')
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(details_table)

    # Build PDF
    doc.build(elements)


@app.route('/success')
def success():
    volunteer_name = request.args.get('name', 'Volunteer')
    return render_template('success.html', volunteer_name=volunteer_name)


if __name__ == '__main__':
    app.run(debug=True)
