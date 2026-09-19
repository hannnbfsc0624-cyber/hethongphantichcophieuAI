from app import create_app
from app.config import FLASK_PORT

app = create_app()

if __name__ == "__main__":
    print(f"🚀 Stock AI System chạy tại: http://localhost:{FLASK_PORT}")
    # use_reloader=False để tránh việc file stock_ai.db (được tạo lúc chạy) làm
    # watchdog tự restart server liên tục. Bật debug=True vẫn giữ traceback đẹp.
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=True, use_reloader=False)
