from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import *
from app.main.forms import *
from app.models import *
# from app.translate import translate
from app.main import bp
from flask import g

from app.models import *
from sqlalchemy import *
from sqlalchemy import create_engine, MetaData, Table, and_, or_
from config import Config
from app.formatText import *
import requests

import subprocess

import os 

from io import BytesIO

import ast
from re import search


"""
        
        request     : The request object, which encapsulates the contents of a HTTP request sent by the
                        client.
        
        current_app : The application instance for the active application.
        
        g           : An object that the application can use for temporary storage during the handling of
                        a request. This variable is reset with each request.    
        
        session     : The user session, a dictionary that the application can use to store values that are
                        “remembered” between requests
                        
                        
"""



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
        g.city_form = CityForm()

        lastcur = HistoryCurrency.query.order_by(HistoryCurrency.id.desc()).first()
        if lastcur != None:
            g.lastcurrency = lastcur.currency
        else:
            g.lastcurrency = 'EUR-UAH'

        lastct = HistoryCity.query.order_by(HistoryCity.id.desc()).first()
        if lastct != None:
            g.lastcity = lastct.city
        else:
            g.lastcity = 'Lviv'
        # print('===================\n',current_user.id,'\n===============')
        g.city = City.query.filter_by(user_id = current_user.id).all()
        # us = User.query.filter_by(id = current_user.id).first()
        if g.city != None:
            g.city = g.city
        else:
            g.city = 'Lviv'

        g.exchangeRate_form = ExchangeRatesForm()

        g.currency = Currency.query.filter_by(user_id = current_user.id).all()
        if g.currency != None:
            g.currency = us.currencies
        else:
            g.currency = 'EUR-UAH'

    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        """pref = Preferences(preferPost = Post.query.order_by(Post.id.desc()).first(),
                                                    science = bool(form.science.data),
                                                    sport = bool(form.sport.data),
                                                    people = bool(form.people.data),
                                                    policy = bool(form.policy.data))
                                db.session.add(pref)
                                db.session.commit()"""
        if form.file.data:
            print(Post.query.order_by(Post.id.desc()).first())
            print("Name saved file: ", form.file.data.name)

            newFile = FileContent(name=form.file.data.filename, data = form.file.data.read(),
                                 postId = Post.query.order_by(Post.id.desc()).first())        

            db.session.add(newFile)
        db.session.commit()

        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    posts = formatLaTeX(posts.items)
    leng = User.query.filter_by(username = current_user.username).first()
    len_post = leng.len_post
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts, next_url=next_url,
                           prev_url=prev_url, len_post = int(len_post))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    posts = formatLaTeX(posts.items)
    leng = User.query.filter_by(username = current_user.username).first()
    len_post = leng.len_post
    return render_template('index.html', title=_('Explore'),
                           posts=posts, next_url=next_url,
                           prev_url=prev_url, len_post = int(len_post))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    leng = User.query.filter_by(username = current_user.username).first()
    len_post = leng.len_post
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, len_post = int(len_post))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.len_post = form.abstract.data
        cities = formatCities(form.city.data)

        del_city = City.query.filter_by(user_id = current_user.id).all()
        for c in del_city:
            db.session.delete(c)
        db.session.commit()

        for ct in cities:
            #current_user.cities.city = form.city.data
            city = City(city=ct, author=current_user)
            db.session.add(city)



        currency = formatCurrency(form.currency.data)

        del_cur = Currency.query.filter_by(user_id = current_user.id).all()
        for c in del_cur:
            db.session.delete(c)
        db.session.commit()

        for cu in currency:
            #current_user.cities.city = form.city.data
            curren = Currency(currency=cu, author=current_user)
            db.session.add(curren)

        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.abstract.data = current_user.len_post

        city = City.query.filter_by(user_id = current_user.id).all()
        ls = []
        for ct in city:
            ls.append(ct.city)
        print(ls)
        form.city.data = ', '.join(ls)

        curr = Currency.query.filter_by(user_id = current_user.id).all()
        ls = []
        if curr != None:
            for cr in curr:
                ls.append(cr.currency)
            print(ls)
            form.currency.data = ', '.join(ls)
        else:
            form.currency.data = 'EUR-USD'

    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/history')
def history():
    histcurr = HistoryCurrency.query.filter_by(user_id = current_user.id).all()
    histcity = HistoryCity.query.filter_by(user_id = current_user.id).all()

    return render_template('history.html', currency = histcurr, city=histcity)





@bp.route('/erp', methods=['GET', 'POST'])
def exchange_rates_rp(cur1,cur2,price):
    form_pr = priceForm()

    currency = '{}-{}'.format(cur1,cur2)
    cur = HistoryCurrency(currency=currency, author=current_user)
    db.session.add(cur)
    db.session.commit()


    print('cur1: {}, cur2: {}, price: {}'.format(cur1,cur2,price))
    url1='http://data.fixer.io/api/latest?access_key=82d9c1133d96a124953ca87e204fb421'
    json_data = requests.get(url1).json()

    # print("exchange_rates_rp",currency)
    bid1 = json_data['rates'][cur1]
    bid2 = json_data['rates'][cur2]
    print('exchange_rates_rp')
    

    res = round(price*(bid2/bid1),2)

    

    print(res,'in exchange_rates_rp')
    # return '1 {} = {} {}'.format(currency[0],bid1/bid2,currency[1])
    return render_template('currency.html',price=price,res=res,cur1=cur1,cur2=cur2,form=form_pr)




@bp.route('/er/<name>', methods=['GET', 'POST'])
def exchange_rates_names(name):
    form = priceForm()
    if request.method == 'POST':
        price = form.price.data
        print('after: ',price)
        cur1 = dict(form.sel1.choices).get(form.sel1.data)
        cur2 = dict(form.sel2.choices).get(form.sel2.data)
        
        print('cur1: {}, cur2: {}, price: {}'.format(cur1,cur2,price))
        #return exchange_rates_rp(cur1,cur2,price)
        return exchange_rates_rp(cur1,cur2,price)



    print('exchange_rates_names: ',name)

    cur = HistoryCurrency(currency=name, author=current_user)
    db.session.add(cur)
    db.session.commit()

    print(dict(form.sel1.choices).get(form.sel1.data))
    currency = name.split('-')
    price = 1
    url1='http://data.fixer.io/api/latest?access_key=82d9c1133d96a124953ca87e204fb421'
    json_data = requests.get(url1).json()

    cur1 = currency[0]
    cur2 = currency[1]
    bid1 = json_data['rates'][cur1]
    bid2 = json_data['rates'][cur2]


    res = round(bid2/bid1,2)
    print('def exchange_rates_names: \n   ',res)
    # return '1 {} = {} {}'.format(currency[0],bid1/bid2,currency[1])
    return render_template('currency.html', price=price,res=res,cur1=cur1,cur2=cur2, form = form)




@bp.route('/er', methods=['GET', 'POST'])
def exchange_rates():
    form = ExchangeRatesForm()
    form_pr = priceForm()
    if request.method == 'POST':
        price = form_pr.price.data
        print('after: ',price)
        cur1 = dict(form_pr.sel1.choices).get(form_pr.sel1.data)
        cur2 = dict(form_pr.sel2.choices).get(form_pr.sel2.data)
        
        print('cur1: {}, cur2: {}, price: {}'.format(cur1,cur2,price))
        #return exchange_rates_rp(cur1,cur2,price)
        return exchange_rates_rp(cur1,cur2,price)


    cur = HistoryCurrency(currency=str(form.currency.data), author=current_user)
    db.session.add(cur)
    db.session.commit()

    currency = str(form.currency.data).split('-')
    price = 1
    url1='http://data.fixer.io/api/latest?access_key=82d9c1133d96a124953ca87e204fb421'
    json_data = requests.get(url1).json()


    bid1 = json_data['rates'][currency[0]]
    bid2 = json_data['rates'][currency[1]]
    cur1 = currency[0]
    cur2 = currency[1]
    

    res = round(bid2/bid1,2)

    print('def  exchange_rates: \n   ',res)
    # return '1 {} = {} {}'.format(currency[0],bid1/bid2,currency[1])
    return render_template('currency.html', price=price,res=res,cur1=cur1,cur2=cur2, form = form_pr)












@bp.route('/city/<name>')
def cityname(name):
    print(name)
    url='https://api.openweathermap.org/data/2.5/weather?q={}&appid=cc7310fa8a816edb333e509044ca5187'.format(name)
    # city = input('City Name :')
    # url = api_address + city

    ct = HistoryCity(city=name, author=current_user)
    db.session.add(ct)
    db.session.commit()

    json_data = requests.get(url).json()
    weat = json_data['weather'][0]['main']
    temp = round(json_data['main']['temp']-273.15, 1)
    sky = json_data['weather'][0]['description']
    icon = json_data['weather'][0]['icon']
    icon = "http://openweathermap.org/img/w/{}.png".format(icon)
    print(icon)
    # weather = formatWeather(round(temp,1),sky,weat,name)
    return render_template('weather.html', city = name,weat = weat, temp=temp, sky=sky, icon=icon)




@bp.route('/city')
def city():
    form = CityForm()
    city = str(form.city.data)
    print(city)

    ct = HistoryCity(city=city, author=current_user)
    db.session.add(ct)
    db.session.commit()

    url='https://api.openweathermap.org/data/2.5/weather?q={}&appid=cc7310fa8a816edb333e509044ca5187'.format(city)
    # city = input('City Name :')
    # url = api_address + city
    json_data = requests.get(url).json()
    weat = json_data['weather'][0]['main']
    temp = round(json_data['main']['temp']-273.15, 1)
    sky = json_data['weather'][0]['description']
    icon = json_data['weather'][0]['icon']
    icon = "http://openweathermap.org/img/w/{}.png".format(icon)
    print(icon)
    # weather = formatWeather(round(temp,1),sky,weat,city)
    return render_template('weather.html', city = city,weat = weat, temp=temp, sky=sky, icon=icon)





@bp.route('/preamble/', methods=['GET', 'POST'])
def preamble():
    form = Preamble()
    if form.validate_on_submit():
        preamble = Preambul(body=form.preamble.data)
        db.session.add(preamble)
        db.session.commit()
        
        flash(_('Your preamble is now live!'))
        return redirect(url_for('main.preamble'))
    pream = Preambul.query.all()
    # print(pream[0].body)
    pream = formatLaTeX(pream)
    return render_template('preamble.html', preamble=pream, form = form)


"""
@bp.route('/preference')
def preference():
    prefU = Preferences.query.filter_by(user_id = current_user.id).first()


    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    newPosts = []
    for post in posts.items:
        prefP = Preferences.query.filter_by(post_id = post.id).first()
        if (prefP.science == prefU.science or
            prefP.sport == prefU.sport or
            prefP.people == prefU.people or
            prefP.policy == prefU.policy):
            newPosts.add(post)

    posts = formatLaTeX(newPosts)
    leng = User.query.filter_by(username = current_user.username).first()
    len_post = leng.len_post

    return render_template('index.html', title=_('Explore'),
                           posts=posts, next_url=next_url,
                           prev_url=prev_url, len_post = int(len_post))



"""



# Show post
@bp.route('/dpost/<post>')
def post(post):
    file = FileContent.query.filter_by(post_id = post).first()
    post = Post.query.filter_by(id = post).first()
    post = formatLaTeX([post])
    print(file)
    if file:
        print('good, this post have file\n')
        
        return render_template('post.html' , post=post[0], file = file)
    else:
        print('this post dont have file\n')
        
        return render_template('post.html' , post=post[0])



@bp.route('/download/<file>')
def download(file):
    file = FileContent.query.filter_by(id = file).first()
    print(file.name)
    return send_file(BytesIO(file.data), attachment_filename=str(file.name))



# Show message
@bp.route('/Show_message/<post>')
def Show_message(post):
    file = FileContent.query.filter_by(message_id = post).first()
    post = Message.query.filter_by(id = post).first()
    post = formatLaTeX([post])
    if file:
        print('good, this message have file\n')
        
        return render_template('post.html' , post=post[0], file = file, recipient = post[0].author.username)
    else:
        print('this message dont have file\n')
        
        return render_template('post.html' , post=post[0], recipient = post[0].author.username)
    #return render_template('post.html' , post=post[0])



@bp.route('/delete_post/<post>')
def delete_post(post):
    post = Post.query.filter_by(id = post).first()
    if current_user.username == post.author.username:
        db.session.delete(post)
        db.session.commit()
        flash('Post delete')
        return user(current_user.username)
    else:
        return user(current_user.username)
    



@bp.route('/latex/<post>')
def pdf_tex(post):
    print('before start LaTeX')
    post = Post.query.filter_by(id = post).first()
    url = r'C:\Users\YURA\eclipse-workspace\microblog\LaTeX_PDF\{}'.format('pdflatex')
    with open('{}.tex'.format(url), 'wb') as f:
        f.write(r'''\documentclass[a4paper,12pt]{article}
\usepackage[ukrainian,english]{babel}
\usepackage[utf8]{inputenc}

\topmargin=-15mm
\textheight=230mm
\begin{document}  
'''.encode('utf8'))
        f.write(post.body.encode('utf8'))
        f.write("\n\end{document}".encode('utf8'))

    commandLine = subprocess.Popen(['pdflatex', '{}.tex'.format(url)])
    commandLine.communicate()

    return send_file('C:/Users/YURA/eclipse-workspace/microblog/pdflatex.pdf',attachment_filename='pdflatex.pdf')
   

   
@bp.route('/searchs')
@login_required
def searchs():
    form = SearchForm()
    search = str(form.q.data)
    print('Search',search)
    filterpost = Post.query.filter(Post.body.like('%{}%'.format(search))).all()
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    
    k=0
    sear = ''
    search = search.split(' ')
    if len(search) >= 1:
        for word in search:
            k += 1
            if k != len(search):
                sear += "body LIKE '%{}%' OR ".format(word)
            else:
                sear += "body LIKE '%{}%'".format(word)
            
    result = connection.execute("SELECT * FROM Post WHERE {};".format(sear))
    list = []
    for row in result:
        list.append(int(row.id))
    pos = Post.query.filter(Post.id.in_(list)).all()
    
    return render_template('searchs.html' , posts=pos)



@bp.route('/<username>/followers')
@login_required
def followeres(username):
    pp = User.query.filter_by(username = username).first()
    print(pp.id)
    
    print('p followers count = ',pp.followers.count())
    return render_template('followers.html', followers=pp.followers)



@bp.route('/<username>/followed')
@login_required
def followed(username):
    pp = User.query.filter_by(username = username).first()
    print(pp.id)
    
    return render_template('followed.html', followeds=pp.followed)



@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))



@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))



@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})





@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)
 

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)



@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        if form.file.data:
            print(Message.query.order_by(Message.id.desc()).first())
            print("Name saved file: ", form.file.data.name)
            newFile = FileContent(name=form.file.data.filename, data = form.file.data.read(),
                                 messageId = Message.query.order_by(Message.id.desc()).first())                
            db.session.add(newFile)
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


    
@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    user = User.query.filter_by(username = current_user.username).first()
    leng = user.len_post
    print(leng)
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, len_post = leng, messageTrue = 1)
  


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])