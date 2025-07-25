from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# for thread
# app.run(host=HOST, port=PORT, threaded=True)