from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, session
from flask_login import current_user, login_required
import requests
from PIL import Image
from io import BytesIO
from frontend.dashboard.utils import sorted_search
import asyncio
from datetime import datetime, timedelta
from frontend.dashboard.forms import AddHabitForm, AttachCategoryForm, AddRelevancyForm, AddNumForm, RecordActivityForm
import json
import math

dash = Blueprint('dash', __name__)


# View Function - Homepage / Search Results
@login_required
@dash.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    if not current_user.is_authenticated:
        flash("The user is not logged in.", 'danger')
        return redirect(url_for('dash.dashboard'))
    form = AddHabitForm()
    if form.validate_on_submit():
        request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['GET_CAT_URL'], json={
            'auth_token': current_user.auth_token,
            'text': form.habit.data
        })
        data = request_data.json()
        return redirect(f"{url_for('dash.attach_category')}?habit={form.habit.data.replace(' ', '+')}")
    return render_template('add_habit.html', form=form)


@login_required
@dash.route('/attach_category', methods=['GET', 'POST'])
def attach_category():
    if not current_user.is_authenticated:
        flash("The user is not logged in.", 'danger')
        return redirect(url_for('dash.dashboard'))

    habit_text = request.args.get('habit', default="")

    form = AttachCategoryForm()

    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['GET_CAT_URL'], json={
        'auth_token': current_user.auth_token,
        'text': habit_text
    })
    data = request_data.json()
    print(data['data'])
    cat_names = [(x[2], x[1]) for x in data['data']]

    form.category.choices = cat_names

    if form.is_submitted():
        return redirect(f"{url_for('dash.add_relevancy')}?habit={habit_text}&cat={form.category.data}")

    form.habit.data = habit_text

    return render_template('attach_category.html', form=form)


@dash.route('/add_relevancy', methods=['GET', 'POST'])
def add_relevancy():
    if not current_user.is_authenticated:
        flash("The user is not logged in.", 'danger')
        return redirect(url_for('dash.dashboard'))

    form = AddRelevancyForm()

    habit_text = request.args.get('habit', default="")
    category = request.args.get('cat', type=int, default=1)

    if form.validate_on_submit():
        return redirect(
            f"{url_for('dash.add_init_num')}?habit={habit_text}&cat={category}&relevancy={form.relevancy.data}")

    form.habit.data = habit_text
    form.category.data = category

    return render_template('add_relevancy.html', form=form)


@dash.route('/add_init_num', methods=['GET', 'POST'])
def add_init_num():
    if not current_user.is_authenticated:
        flash("The user is not logged in.", 'danger')
        return redirect(url_for('dash.dashboard'))

    form = AddNumForm()

    habit_text = request.args.get('habit', default="")
    category = request.args.get('cat', type=int, default=1)
    relevancy = request.args.get('relevancy', type=int, default=1)

    if form.is_submitted():
        request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_HABIT_URL'], json={
            'auth_token': current_user.auth_token,
            'habit_name': habit_text,
            'pref_level': relevancy,
            'cat_id': category,
            'curr_num': form.init_num.data
        })
        data = request_data.json()
        if data['status'] == 1:
            flash("Habit added successfully!", 'success')
        else:
            flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))

    form.habit.data = habit_text
    form.category.data = category
    form.relevancy.data = relevancy

    return render_template('add_num.html', form=form)


@login_required
@dash.route('/', methods=['GET'])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('common.login'))
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['USER_HABIT_DATA_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    habit_data = request_data.json()['data']

    habit_list = []

    curr_date = datetime.now()
    date_list = [((curr_date - timedelta(days=x)).strftime("%m-%d-%y")) for x in range(0, 7)]

    for each_habit in habit_data:
        habit_list.append({
            'name': each_habit['name'],
            'level': math.floor(each_habit['curr_num'] / each_habit['init_num']),
            'level_progress': math.floor((each_habit['curr_num'] % each_habit['init_num']) * 100),
            'num_left': (each_habit['curr_target'] if each_habit['curr_target'] is not None else 0) -
                        each_habit['num_today'].get(datetime.now().strftime("%m-%d-%y"), 0),
            'data': [each_habit['num_today'].get(x, 0) for x in date_list]
        })

    return render_template('index.html', habit_list=habit_list, date_list=date_list)


@login_required
@dash.route('/record_activity', methods=['GET', 'POST'])
def record_activity():
    form = RecordActivityForm()

    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['USER_HABIT_DATA_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    habit_data = request_data.json()['data']

    habit_list = [(x['id'], x['name']) for x in habit_data]

    form.habit.choices = habit_list

    if form.is_submitted():
        request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['RECORD_ACTIVITY_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'habit_id': form.habit.data
                                     })
        data = request_data.json()
        if data['status'] == 1:
            flash("Activity Recorded Successfully!", 'success')
        else:
            flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('report_activity.html', form=form)


@login_required
@dash.route('/expert_help', methods=['GET', 'POST'])
def show_expert_help_info():
    return render_template('helpers.html')
