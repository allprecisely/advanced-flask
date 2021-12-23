from app import app, jwt
from db import db, jwt_redis_blocklist, ACCESS_EXPIRES

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def check_id_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
