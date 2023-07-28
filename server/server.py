from app import app
from routes import auth, translation, data

# Route for the root endpoint
@app.route('/')
def root():
    return "Welcome to the root!"

if __name__ == '__main__':
    app.run(debug=True)
