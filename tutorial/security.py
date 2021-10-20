import bcrypt
from pyramid.authentication import AuthTktCookieHelper


# def hash_password(pw):
#     pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
#     return pwhash.decode('utf8')

# def check_password(pw, hashed_pw):
#     expected_hash = hashed_pw.encode('utf8')
#     return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

# from .models import DBSession, SanPham, NhanVien

USERS = {}

# # USERS = {}
# sanphams = DBSession.query(SanPham)
# for sanpham in sanphams:
#     print(sanpham.__dict__)
# def changeToDict():
    # nhanviens = DBSession.query(NhanVien)
    # for nhanvien in nhanviens:
    #     USERS.update(nhanvien.__dict__)
#     return USERS

# changeToDict()

# print(USERS)

class SecurityPolicy:
    def __init__(self, secret):
        self.authtkt = AuthTktCookieHelper(secret=secret)


    def identity(self, request):
        identity = self.authtkt.identify(request)
        if identity is not None and identity['userid'] in USERS:
            return identity

    def authenticated_userid(self, request):
        identity = self.identity(request)
        if identity is not None:
            return identity['userid']

    def remember(self, request, userid, **kw):
        return self.authtkt.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.authtkt.forget(request, **kw)