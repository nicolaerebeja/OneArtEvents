from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required

from website.models import db, User

@login_required
def userIndex():
    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')

            user = User.query.get(user_id)

            if user:
                if 'delete' in request.form:
                    db.session.delete(user)
                else:
                    if user.type == 'new':
                        user.type = 'admin'

                db.session.commit()

                return redirect(url_for('views.userIndex'))
            else:
                return jsonify({'message': 'Error'}), 404

        except Exception as e:
            return jsonify({'message': 'Error', 'error_details': str(e)}), 500


    all_users = User.query.all()
    return render_template("admin/users.html", users=all_users)


@login_required
def profilDansator(user_id):
    user = User.query.get(user_id)
    return render_template("admin/profil-dansator.html", dansator=user)
