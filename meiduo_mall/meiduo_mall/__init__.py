import pymysql

# MySQLdb不支持python3,用pymysql做初始化
pymysql.install_as_MySQLdb()