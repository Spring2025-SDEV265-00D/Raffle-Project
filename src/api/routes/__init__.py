from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .seller_routes import seller_bp
from .cashier_routes import cashier_bp
from .fetcher_routes import fetcher_bp
blueprints = [auth_bp,
              admin_bp,
              seller_bp,
              cashier_bp,
              fetcher_bp]
