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



