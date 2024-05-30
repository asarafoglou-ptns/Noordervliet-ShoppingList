from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    '''This is the home page, which showcases the text "Hello, World!"'''
    return 'Hello, World!'

@app.route('/login')
def login():
    '''This is the login page, which showcases the text "Welcome to the login page!"'''	
    return 'Welcome to the login page!'

if __name__ == '__main__':
    app.run(debug=True)