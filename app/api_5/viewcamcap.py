from flask import jsonify,request,g,abort,url_for,json
from .. import db
from ..models import SVSIpCamReg,SVSuserReg,SVSFaceTab,current_app
from . import api_5
from .decorators import permission_required
from .errors import forbidden
from cryptography.fernet import Fernet
from flask.ext.login import login_user, logout_user, login_required,current_user
from base64 import b64encode
import  base64

@api_5.route('/viewfaces')
def get_userfaces():
    page = request.args.get('page', 1, type=int)
    email = SVSuserReg.query.filter_by(emid=g.current_user.emid).first()
    pagination = SVSFaceTab.query.filter_by( u_id = email.id ).order_by(SVSFaceTab.Face_save_date.desc()).paginate(page, per_page=current_app.config['SVS_PAGE_PHOTO'],error_out=False)
    photos = pagination.items
    for rec in photos:
        camfacesimag=rec.Face_image
        testb64 = b64encode(camfacesimag)
        #rec.Face_image = json.loads(unicode(opener.open(...), "ISO-8859-1"))
        #rec.Face_imagenew= base64.decodestring(json.dumps(camfacesimag)['image'])
        rec.Face_image = testb64
    prev = None
    if pagination.has_prev:
        prev = url_for('api_5.get_userfaces', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api_5.get_userfaces', page=page+1, _external=True)

    return jsonify({
        'posts': [recphotos.to_json() for recphotos in photos],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
