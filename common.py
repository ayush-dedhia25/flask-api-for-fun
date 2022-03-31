# ===========================================================
# Common Extension File (a.k.a Shared Files)
# ===========================================================
# Common Configurations Stored Here.
# This file contains all the shared data to be use across the
# application state.
#
# @Author `Ayush Dedhia <ayushdedhia25@gmail.com>`
# @License `UNLICENSED`
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Database connection pool
database = SQLAlchemy()

# Timestamp Mixin
class TimestampMixin(object):
   createdAt = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
   updatedAt = database.Column(database.DateTime, onupdate=datetime.utcnow)