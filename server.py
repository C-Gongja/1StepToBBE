from app import create_app

app = create_app()

if __name__ == "__main__":
    print("🚀 Start GraphQL + REST API Hybrid Server!")
    print("📊 GraphQL Endpoint: http://localhost:5000/graphql")
    print("🔗 REST API Endpoint: http://localhost:5000/api/v1")
    print("❤️ Health Check: http://localhost:5000/health")

    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))

# for thread
# app.run(host=HOST, port=PORT, threaded=True)
