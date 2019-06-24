from flask import request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import *
import requests



class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    abstract = IntegerField(_l('Length posts'), validators=[DataRequired()])
    city = StringField(_l('Cities'), validators=[DataRequired(),Length(min=0, max=140)])
    currency = StringField(_l('Currency'), validators=[DataRequired(),Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class Preamble(FlaskForm):
    preamble = TextAreaField(_l('Write you preamble'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


# Форма для постів
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    file = FileField(_l('File'))
    submit = SubmitField(_l('Submit')) 


# Форма для коментарів
class CommentForm(FlaskForm):
    comment = TextAreaField(_l('Say comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit')) 
    
    

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
        


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    file = FileField(_l('File'))
    submit = SubmitField(_l('Submit'))


class CityForm(FlaskForm):
    city = StringField(_l('City'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(CityForm, self).__init__(*args, **kwargs)



class ExchangeRatesForm(FlaskForm):
    currency = StringField(_l('UAH-USD'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(ExchangeRatesForm, self).__init__(*args, **kwargs)

class priceForm(FlaskForm):
    url1='http://data.fixer.io/api/latest?access_key=82d9c1133d96a124953ca87e204fb421'
    json_data = requests.get(url1).json()
    ch = [(str(akey), str(akey)) for akey in json_data['rates']]

    # print(ch)
    sel1 =  SelectField(u'Currency', choices = ch)
    sel2 =  SelectField(u'Currency', choices = ch)


    price = IntegerField(_l('price'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

"""    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(priceForm, self).__init__(*args, **kwargs)
"""
        
