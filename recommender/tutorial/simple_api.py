from flask import Flask, request

app = Flask(__name__)

# This defines a simple get request from root.
@app.route('/')
def sample_get():
    return "Hello, visitor!"

#This defines a simple get request in sub directory 'sub'.
@app.route('/sub/')
def sample_get_sub():
    return "Hello, visitor! You entered a sub directory."

#This defines a simple get request in sub directory 'sub', where 'arg' is an argument.
@app.route('/sub/<arg>')
def sample_get_with_arg(arg):
    return "Hello, visitor! You entered a sub directory with argument '" + arg + "'."

#This defines a simple post request.
@app.route('/', methods = ['POST'])
def sample_post():
    return "You posted '" + request.data + "'."

if (__name__ == "__main__"):
    app.run()