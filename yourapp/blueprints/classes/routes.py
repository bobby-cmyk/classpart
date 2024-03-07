import os
from flask import render_template, request, redirect, url_for, flash, current_app, session, jsonify, Response, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import csv
from yourapp.helper import validate_csv_headers
from yourapp.models import db, Class, Student, class_enrollment, Participation
from io import StringIO
import pytz
from sqlalchemy.exc import SQLAlchemyError

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    if request.method == 'POST':
        class_name = request.form['class_name']
        file = request.files['file']

        if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
            flash('Invalid file type. Please upload a CSV file.', 'warning')
            return redirect(url_for('classes.classes'))

        filename = secure_filename(file.filename)
        uploads_dir = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)

        new_class = Class(name=class_name, user_id=current_user.id)
        db.session.add(new_class)
        db.session.flush()

        expected_headers = ['name', 'id', 'group']
        if not validate_csv_headers(filepath, expected_headers):
            os.remove(filepath)  # Delete the file if headers are invalid
            flash('Invalid CSV format. Expected headers: name, id, group.', 'warning')
            return redirect(url_for('classes.classes'))

        try:
            with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student = Student.query.filter_by(student_id=row['id']).first()
                    if not student:
                        student = Student(name=row['name'], student_id=row['id'], group=row['group'])
                        db.session.add(student)
                    new_class.students.append(student)
            db.session.commit()
            flash('Successfully created new class!', 'success')
        except csv.Error as e:
            flash(f'Error processing CSV file. {str(e)}', 'danger')
            return redirect(url_for('classes.classes'))
        finally:
            os.remove(filepath)  # Ensure the file is deleted after processing

        return redirect(url_for('classes.classes'))

    all_classes = Class.query.filter_by(user_id=current_user.id).all()
    return render_template('classes.html', classes=all_classes)

@classes_bp.route('/start-class/<int:class_id>')
@login_required
def start_class(class_id):
    session['current_class_id'] = class_id  # Set the current class ID in the session
    flash('Class started successfully!', 'success')
    return redirect(url_for('general.index'))

@classes_bp.route('/end-class')
@login_required
def end_class():
    session.pop('current_class_id', None)  # Remove the current_class_id from session
    flash('Class session ended successfully.', 'info')
    return redirect(url_for('general.index'))

@classes_bp.route('/add-participation/<int:student_id>', methods=['POST'])
@login_required
def add_participation(student_id):
    score = request.form.get('score')
    remarks = request.form.get('remarks')

    # Ensure score is within 1-10
    if not (1 <= int(score) <= 10):
        return jsonify({'error': 'Score must be between 1 and 10'}), 400

    participation = Participation(score=score, remarks=remarks, student_id=student_id)
    db.session.add(participation)
    db.session.commit()

    return jsonify({'message': 'Participation added successfully'}), 200

@classes_bp.route('/export/class-participation/<int:class_id>')
@login_required
def export_class_participation(class_id):
    class_ = Class.query.get_or_404(class_id)

    # Prepare CSV output
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['group', 'name', 'id', 'score', 'remarks', 'time'])  # Header

    # Assuming you have relationships set up to access students and their participations
    for student in class_.students:
        for participation in student.participations:
            utc_timestamp = participation.timestamp.replace(tzinfo=pytz.utc)
            localized_timestamp = utc_timestamp.astimezone(pytz.timezone('Asia/Singapore'))

            cw.writerow([
                student.group,
                student.name,
                student.student_id,
                participation.score,
                participation.remarks,
                localized_timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
            ])

    output = si.getvalue()
    si.close()

    # Return the CSV file
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=class_{class_id}_participation.csv"})


@classes_bp.route('/delete-class/<int:class_id>')
@login_required
def delete_class(class_id):
    try:
        class_to_delete = Class.query.get_or_404(class_id)
        student_ids = [student.id for student in class_to_delete.students]

        # First, find students who are only enrolled in this class and no others.
        # This can be determined by checking the length of their 'classes' backref list.
        students_to_delete = [student for student in class_to_delete.students if len(student.classes) == 1]

        # Attempt to delete participations related to students in this class.
        if student_ids:
            Participation.query.filter(Participation.student_id.in_(student_ids)).delete(synchronize_session='fetch')

        # Commit after deleting participations to ensure data consistency.
        db.session.commit()

        # Delete class enrollments related to the class.
        # This needs to be done before attempting to delete the students or the class itself.
        db.session.execute(class_enrollment.delete().where(class_enrollment.c.class_id == class_id))
        db.session.commit()

        # Delete students who are only enrolled in this class.
        for student in students_to_delete:
            db.session.delete(student)

        # Commit the student deletions.
        db.session.commit()

        # Delete the class itself.
        db.session.delete(class_to_delete)
        db.session.commit()

        flash('Class, related participations, and exclusively enrolled students have been deleted.', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        flash('An error occurred while deleting the class. Please try again.', 'error')

    return redirect(url_for('classes.classes'))

