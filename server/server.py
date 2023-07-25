from app import app

@app.route('/')
def root():
    return "Welcome to the root!"

if __name__ == '__main__':
    app.run(debug=True)
