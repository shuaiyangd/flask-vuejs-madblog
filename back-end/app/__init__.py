from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from redis import Redis
from elasticsearch import Elasticsearch
import rq


# Flask-SQLAlchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()
# Flask-Mail plugin
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_app(app, config_class)
    # Enable CORS
    CORS(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)
    # Init Flask-Mail
    mail.init_app(app)

    # 注册 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


def configure_app(app, config_class):
    app.config.from_object(config_class)
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False
    # 整合RQ任务队列
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('madblog-tasks', connection=app.redis, default_timeout=3600)  # 设置任务队列中各任务的执行最大超时时间为 1 小时
    # Elasticsearch全文检索
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


from app import models
