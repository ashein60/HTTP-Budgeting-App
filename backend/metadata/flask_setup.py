from flask import Flask

# This cannot be created in main
# It should not be re-created in each controller class
app = Flask(__name__)