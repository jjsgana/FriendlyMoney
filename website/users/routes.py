from flask import Blueprint, render_template, flash, redirect, request, url_for
from website import db
from website.users.forms import *
from website.models import *
from website.users.utils import *
from flask_login import current_user, login_required
from datetime import timedelta
from datetime import datetime
from website.config import Config

users = Blueprint('users', __name__)

@users.route('/profileinfo_1/<int:user_id>', methods=['GET','POST'])
def profileinfo_1(user_id):

    form = ProfileInfo_1()
    userinfo = User.query.get_or_404(user_id)

    block_user = block_page_when_user_is_hidden(userinfo, user_id)
    if block_user == 'blocked':
        return redirect(url_for('main.home'))


    #tot_exchanges = len(Rate.query.filter_by(userid_receiving=user_id).all()) + len(Rate.query.filter_by(userid_giving=user_id).all())
    tot_positive_rates = len(Rate.query.filter_by(userid_receiving=user_id,rate="Positive").all())
    tot_negative_rates = len(Rate.query.filter_by(userid_receiving=user_id,rate="Negative").all())
    tot = tot_positive_rates + tot_negative_rates

    if tot_positive_rates + tot_negative_rates == 0:
        userhasreviews = False
    else:
        userhasreviews = True

    if Rate.query.filter_by(userid_giving=user_id).order_by(Rate.rate_date.desc()).first() != None:
        last_exchange = Rate.query.filter_by(userid_giving=user_id).order_by(Rate.rate_date.desc()).first().rate_date
        last_exchange = last_exchange.strftime('%d-%m-%Y')
    elif Rate.query.filter_by(userid_receiving=user_id).order_by(Rate.rate_date.desc()).first() != None:
        last_exchange = Rate.query.filter_by(userid_receiving=user_id).order_by(Rate.rate_date.desc()).first().rate_date
        last_exchange = last_exchange.strftime('%d-%m-%Y')
    else:
        last_exchange = ''

    items_per_page=5
    page = request.args.get('page', 1, type=int)
    rates = Rate.query.filter_by(userid_receiving=user_id).order_by(Rate.rate_date.desc()).paginate(page=page,per_page=items_per_page)
    items = [row.__dict__ for row in rates] # trasnform rows from Users in a List with each row as Dict
    #print(tot)
    if tot >= items_per_page+1:
        hide_paginator = False
    else:
        hide_paginator = True

    if form.validate_on_submit():
        return redirect(url_for('users.profileinfo_2', user_id=user_id))
    return render_template("profileinfo_1.html",
                            form=form,
                            userinfo=userinfo,
                            #tot_exchanges = tot_exchanges,
                            tot_positive_rates = tot_positive_rates,
                            tot_negative_rates = tot_negative_rates,
                            last_exchange = last_exchange,
                            items=items,
                            rates=rates,
                            user_id=user_id,
                            userhasreviews=userhasreviews,
                            hide_paginator=hide_paginator)


@users.route('/profileinfo_2/<int:user_id>', methods=['GET','POST'])
@login_required
def profileinfo_2(user_id):
    userinfo = User.query.get_or_404(user_id)
    block_user = block_page_when_user_is_hidden(userinfo, user_id)
    if block_user == 'blocked':
        return redirect(url_for('main.home'))


    form = ProfileInfo_2()
    if form.validate_on_submit():
        current_user_is_hidden = User.query.filter_by(id=current_user.get_id()).first().account_hidden
        if current_user_is_hidden == True:
            flash(f"You can't rate a user if your account is hidden, please unhide it", 'warning')
            return redirect(url_for('main.myapp'))

        return redirect(url_for('users.rate', user_id=user_id))
    return render_template("profileinfo_2.html", form=form, userinfo=userinfo)


@users.route('/rate_user/<int:user_id>', methods=['GET','POST'])
@login_required
def rate(user_id):
    #test = Rate.query.filter_by(userid_giving=current_user.get_id()).order_by(Rate.rate_date.desc()).first().rate_date
    #print(test)

    userinfo = User.query.get_or_404(user_id) # info. of user receiving the rate
    selfrating = int(current_user.get_id()) == int(userinfo.id) # current_user is the logged in user | userinfo is user who'll receive a rate
    form = RateUser()

    block_user = block_page_when_user_is_hidden(userinfo, user_id)
    if block_user == 'blocked':
        return redirect(url_for('main.home'))

    def user_able_to_rank_again(hours=Config.TIME_ABLE_RANK_AGAIN):
        user_firs_time_rating = Rate.query.filter_by(userid_giving=current_user.get_id()).order_by(Rate.rate_date.desc()).first() == None
        if user_firs_time_rating == True:
            print('first time user doing a rate')
            return True,0
        else:
            logged_user_last_rate_date = Rate.query.filter_by(userid_giving=current_user.get_id()).order_by(Rate.rate_date.desc()).first().rate_date
            user_able_to_rank_again = logged_user_last_rate_date + timedelta(hours=hours)
            posible_to_rank_again = user_able_to_rank_again < datetime.utcnow()
            time_remaining = abs( (datetime.utcnow()-user_able_to_rank_again) )
            #print('user have already rated before!')
            return posible_to_rank_again,time_remaining

    x = user_able_to_rank_again()

    if form.validate_on_submit():
        input_from_form = Rate(
        rate = form.positive_or_negative.data,
        user_giving_rate_curr = form.user_giving_rate_curr.data,
        user_receving_rate_curr = form.user_receving_rate_curr.data,
        comments = form.comments.data,
        userid_giving = current_user.get_id(),
        userid_receiving = user_id,
        name_surname_giving = (current_user.name + " " + current_user.surname),
        name_surname_receving = (userinfo.name + " " + userinfo.surname)
        )
        
        db.session.add(input_from_form)
        db.session.commit()
        send_notification_when_rating(giving_rate_user=current_user, receving_rate_user=userinfo)
        flash(f"Thank you {current_user.name}! You have rated user {userinfo.name}", 'success')
        return redirect(url_for('main.home'))

    return render_template("rate_user.html", form=form, userinfo=userinfo, selfrating=selfrating, able_rankagain=x[0], time_remaining=x[1])