from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required



@login_required
def analytics():
    return render_template("admin/analytics.html")