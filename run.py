from flaskblog import create_app

# if you want a custom config pass it in here, otherwise it will use our default
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)