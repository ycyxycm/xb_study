import os

# ================================================= #
# *************** mysql数据库 配置  *************** #
# ================================================= #
# 数据库 ENGINE ，默认演示使用 sqlite3 数据库，正式环境建议使用 mysql 数据库
# sqlite3 设置
# DATABASE_ENGINE = "django.db.backends.sqlite3"
# DATABASE_NAME = os.path.join(BASE_DIR, "db.sqlite3")

# 使用mysql时，改为此配置
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_NAME = 'xb_system' # mysql 时使用

# 数据库地址 改为自己数据库地址
DATABASE_HOST = "XXXXXXXX"
# # 数据库端口5
DATABASE_PORT = 3306
# # 数据库用户名
DATABASE_USER = "root"
# # 数据库密码
DATABASE_PASSWORD = "XXXXXXXX"

#邮箱授权码
EMAIL_IMAPSMTP="XXXXXXXX"
EMAIL="XXXXXXXX"

# 表前缀
# TABLE_PREFIX = "dvadmin_"
# ================================================= #
# ******** redis配置，无redis 可不进行配置  ******** #
# ================================================= #
REDIS_PASSWORD = 'XXXXXXXX'
REDIS_HOST = 'XX.XXX.XXX.XX'
REDIS_PORT = 6379
REDIS_DB = 2
# REDIS_URL_DEFAULT = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'
REDIS_URL_DEFAULT = f'redis://{REDIS_HOST}:{REDIS_PORT}/4'
REDIS_URL_SESSION = f'redis://{REDIS_HOST}:{REDIS_PORT}/5'
REDIS_URL_VCODE = f'redis://{REDIS_HOST}:{REDIS_PORT}/6'
#Redis session有效期
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14 #14天有效期
# ================================================= #
# ****************** 功能 启停  ******************* #
# ================================================= #
DEBUG = True
# 启动登录详细概略获取(通过调用api获取ip详细地址。如果是内网，关闭即可)
# ENABLE_LOGIN_ANALYSIS_LOG = True
# 登录接口 /api/token/ 是否需要验证码认证，用于测试，正式环境建议取消
# LOGIN_NO_CAPTCHA_AUTH = True
# ================================================= #
# ****************** 其他 配置  ******************* #
# ================================================= #

ALLOWED_HOSTS = ["*"]
#LOGGING配置

# daphne启动命令
#daphne application.asgi:application -b 0.0.0.0 -p 8000
