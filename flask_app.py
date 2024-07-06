from TaskManager import app,create_database

if __name__ == '__main__':
    create_database()
    app.run(debug=True)

