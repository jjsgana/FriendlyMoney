from flask import Blueprint, render_template, flash, redirect, request, url_for
from website import db
from website.main.forms import *
from website.models import *
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET','POST'])
def home():

    form = Home()
    items_per_page=5
    page = request.args.get('page', 1, type=int)
    user = User.query.order_by(User.register_date.desc()).paginate(page=page,per_page=items_per_page)
    items = [row.__dict__ for row in user] # trasnform rows from Users in a List with each row as Dict
    for item in items:
        tot_positive_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Positive").all())
        tot_negative_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Negative").all())
        item["tot_positive_rates"] = tot_positive_rates
        item["tot_negative_rates"] = tot_negative_rates

    if form.validate_on_submit():

        if form.submit.data:
            search_page = request.args.get('search_page', 1, type=int)
            if len(form.name.data) > 0: # when user search by name
                
                search = "%{}%".format(form.name.data)
                user = User.query.filter(User.name.like(search)).paginate(page=search_page,per_page=items_per_page)
                items = [row.__dict__ for row in user]
                for item in items:
                    tot_positive_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Positive").all())
                    tot_negative_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Negative").all())
                    item["tot_positive_rates"] = tot_positive_rates
                    item["tot_negative_rates"] = tot_negative_rates
                flash(f'Searched by Name', 'success')
                return render_template("home.html", form=form, items=items, user=user, buttonsearch=1)
            
            elif len(form.ineed.data) > 0: # when user search by I need

                offrcurr = "%{}%".format(form.ineed.data)
                user = User.query.filter(User.offrcurr.like(offrcurr)).paginate(page=search_page,per_page=items_per_page)
                items = [row.__dict__ for row in user]
                for item in items:
                    tot_positive_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Positive").all())
                    tot_negative_rates = len(Rate.query.filter_by(userid_receiving=item["id"],rate="Negative").all())
                    item["tot_positive_rates"] = tot_positive_rates
                    item["tot_negative_rates"] = tot_negative_rates
                flash(f'Searched by Currency', 'success')
                return render_template("home.html", form=form, items=items, user=user, buttonsearch=1)

            else: # user don't put any input
                return redirect(url_for('main.home'))
        
    return render_template("home.html", form=form, items=items, user=user,search=0)


@main.route('/myapp', methods=['GET','POST'])
@login_required
def myapp():
    form = MyApp()
    needcurr = request.form.getlist('needcurr')
    offrcurr = request.form.getlist('offercurr')
    

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.fb = form.fb.data
        current_user.wa = form.wa.data
        current_user.needcurr = ','.join(needcurr)
        current_user.offrcurr = ','.join(offrcurr)
        current_user.last_update_date = datetime.utcnow()
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.fb.data = current_user.fb
        form.wa.data = current_user.wa

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
    return render_template("myapp.html", image_file=image_file, form=form)