"""
    Format post.body for pdf and LaTeX file
"""
import re

def insert_dash(string, index,paste):
    return string[:index] + paste + string[index:]

def formatLaTeX (posts):
    for post in posts:

        # for commit (%.....\n)
        procent = []
        enter = []
        for i in range(len(post.body)):
            if post.body[i] == '%' and post.body[i-1] == '\n':
                procent.append(i)
                enter.append(post.body[i+1:].index('\n'))
        for j in range(len(procent)):
            post.body = insert_dash(post.body,procent[j] + (j * 39),'<span style="color:gray"><i>')
            post.body = insert_dash(post.body,enter[j] + 28 + procent[j] + (j * 39),'</i></span>')

                

        post.body = post.body.replace( "\n","<br>") # \n
        post.body = post.body.replace('$$', '<span style="color:red;"><br>$$</span>') # $$
        # post.body = post.body.replace('$', '<span style="color:red;"><br>$</span>') # $
        post.body = post.body.replace('\\begin','<span style="color:blue;"><b><br>\\begin</b></span>') # \begin 
        post.body = post.body.replace('\end','<span style="color:blue;"><b><br>\end</b></span>') # \end

        post.body = post.body.replace('equation','<b style="color:#009933">equation</b>') # equation 
    return posts


def formatWeather (temp,sky,weat,city):
    
    weather = '<span style="color:orange;">Температура: {}</span>'.format(temp) 
    weather = '<span style="color:blue;">Небо: {} </span><br>'.format(sky) + weather
    weather = '<span style="color:#59a680;">Погода: {}</span> <br>'.format(weat) + weather
    weather = '<span style="color:black;">Місто: {}</span> <br>'.format(city) + weather

    return weather

def formatCities(cities):
    #cities = re.split(r'\s{1,}', cities)
    cities = cities.split(', ')
    return cities

def formatCurrency(currency):
    #cur = re.split(r'\s{1,}', currency)
    currency = currency.split(', ')
    return currency

def formatCurForHTML(price,bid1,bid2,cur1,cur2):
    res = '{} {} = {} {}'.format(price, cur1,round(price*(bid2/bid1),2),cur2)