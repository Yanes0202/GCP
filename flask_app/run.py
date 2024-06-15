import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from flask_app.flask_endpoint import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
