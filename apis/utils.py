import hashlib
from functools import wraps

import maya
import phonenumbers
from flask import request , jsonify , g

from apis.models import db, UserIdentities


def authenticate_request(**options):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            mobile = get_mobile(request.headers.get('mobile'))

            if not mobile:
                return jsonify({"Error": 'Please Provide Mobile Number'}), 412

            user_identity = db.session.query(UserIdentities).filter(
                UserIdentities.identity == mobile,
                UserIdentities.identity_type == 'Author',
                UserIdentities.row_status == 'active').first()

            if not user_identity:
                return jsonify({"Error": "Authorization failed."}), 412
            pasw = request.headers.get('password')
            if not pasw:
                return jsonify({"Error": 'Enter Password'}), 412
            pasw = hashlib.sha256(pasw.encode()).hexdigest()
            if pasw != user_identity.password:
                return jsonify({"Error": "Incorrect Password"}), 412
            g.triggered_by = user_identity.id
            return f(user_identity.id, *args, **kwargs)
        return wrapper

    return decorator


def get_mobile(mobile):
    mobile = mobile.strip() if mobile else None
    if mobile:
        try:
            mobile = phonenumbers.parse(mobile, 'IN')
            return '+' + str(mobile.country_code) + str(mobile.national_number)
        except phonenumbers.NumberParseException:
            return None
