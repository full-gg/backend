from runtime.listener import app
from runtime.scheduler import scheduler
import os

if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run("0.0.0.0", port=os.getenv('PORT', 6969))
