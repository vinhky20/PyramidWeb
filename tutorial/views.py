import colander
import transaction
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
)

from pyramid.security import (
    remember,
    forget,
)

from .security import SecurityPolicy

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .security import (
    USERS,
    GROUPS
)

from .models import DBSession, SanPham, NhanVien, DanhMuc, ChiTietHDBH, ChiTietHDNH


@view_defaults(renderer='home.pt')
class Home:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home')
    def home(self):
                
        return {'name': 'CỬA HÀNG NỘI THẤT'}
            

    @view_config(route_name='login', renderer='login.pt')
    @forbidden_view_config(renderer='login.pt')
    def login(self):
        request = self.request

        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''

        def changeToDict():
            nhanviens = DBSession.query(NhanVien).all()
            nvs = []
            for nhanvien in nhanviens:
                tnv = nhanvien.__dict__
                nvs.append(tnv)
            grp = {}
            urs = {}
            for x in nvs:
                urs[x['username']] = x['password']
                grp[x['username']] = ['group:editors']
            USERS.update(urs)
            GROUPS.update(grp)

            return USERS,GROUPS
        
        changeToDict()

        # print(USERS[userid])

        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            hashed_pw = USERS.get(login)
            if hashed_pw:
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                 headers=headers)
            message = 'Failed login'


        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)

    @view_config(route_name='register', renderer='register.pt')
    def register(self):
        request = self.request
        if 'form.save' in request.params:
            name = request.params['name']
            username = request.params['username']
            password = request.params['password']

            DBSession.add(NhanVien(tennhanvien=name, username=username, password=password))
            
            headers = forget(request)
            url = request.route_url('login')
            return HTTPFound(location=url,
                         headers=headers)
        return {
            'status': 'Đăng ký thành công!'
        }

    @view_config(route_name='manageAcc', renderer="manageAcc.pt", permission='edit')
    def manageAcc(self):
        request = self.request
        un = request.authenticated_userid
        # print(un)
        nhanvien = DBSession.query(NhanVien).filter_by(username=un).one()

        if 'form.update' in request.params:
            fullname = request.params['fullname']
            username = request.params['username']
            password = request.params['password']

            nhanvien.tennhanvien = fullname
            nhanvien.username = username
            nhanvien.password = password
            transaction.commit();
            
            headers = forget(request)
            url = request.route_url('home')
            return HTTPFound(location=url,
                         headers=headers)

        if 'form.delete' in request.params:
            DBSession.query(NhanVien).filter_by(username=un).delete()

            headers = forget(request)
            url = request.route_url('home')
            return HTTPFound(location=url,
                         headers=headers)

        return dict(nhanvien=nhanvien)

class ManageProduct:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='sanpham', renderer='sp/sanpham.pt', permission='edit')
    def showsanpham(self):
        request = self.request
        sanphams = DBSession.query(SanPham)
        for sanpham in sanphams:
            print(type(sanpham))
        return dict(sanphams=sanphams)

    @view_config(route_name='ban', renderer='sp/ban.pt')
    def showban(self):
        sanphams = DBSession.query(SanPham).filter_by(id_dm=2)
        # for sanpham in sanphams:
        #     print(sanpham.__dict__)
        return dict(sanphams=sanphams)

    @view_config(route_name='sofa', renderer='sp/sofa.pt')
    def showsofa(self):
        sanphams = DBSession.query(SanPham).filter_by(id_dm=1)
        # for sanpham in sanphams:
        #     print(sanpham.__dict__)
        return dict(sanphams=sanphams)

    # @property
    # def counter(self):
    #     session = self.request.session
    #     if 'counter' in session:
    #         session['counter'] += 1
    #     else:
    #         session['counter'] = 1

    #     return session['counter']

    @view_config(route_name='addsanpham', renderer='sp/addsanpham.pt')
    def addsanpham(self):
        request = self.request
        if 'form.add' in request.params:
            tensanpham = request.params['tensp']
            dvt = request.params['dvt']
            danhmuc = request.params['danhmuc']

            dm = DBSession.query(DanhMuc).filter_by(tendanhmuc=danhmuc).one()
            id_dm = dm.id_dm

            DBSession.add(SanPham(tensanpham=tensanpham, donvitinh=dvt, id_dm=id_dm))
            
            headers = forget(request)
            url = request.route_url('sanpham')
            return HTTPFound(location=url,
                         headers=headers)
        return {
            'status': 'Thêm sản phẩm thành công!'
        }

    @view_config(route_name='deletesp', renderer='sp/sanpham.pt')
    def deletesp(self):
        request = self.request
        if 'form.delete' in request.params:
            id_sp = request.params['id_sp']

            DBSession.query(SanPham).filter_by(id_sp=id_sp).delete()
            
            headers = forget(request)
            url = request.route_url('sanpham')
            return HTTPFound(location=url,
                         headers=headers)
        return {
            'status': 'Thêm sản phẩm thành công!'
        }

    @view_config(route_name='updatesp', renderer='sp/updatesp.pt')
    def updatesp(self):
        request = self.request
        id_sp = int(self.request.matchdict['id_sp'])
        sanpham = DBSession.query(SanPham).filter_by(id_sp=id_sp).one()


        if 'form.update' in request.params:
            tensanpham = request.params['tensp']
            dvt = request.params['dvt']
            danhmuc = request.params['danhmuc']

            dm = DBSession.query(DanhMuc).filter_by(tendanhmuc=danhmuc).one()
            id_dm = dm.id_dm
            sanpham.tensanpham = tensanpham
            sanpham.donvitinh = dvt
            sanpham.id_dm = id_dm
            transaction.commit();
            
            headers = forget(request)
            url = request.route_url('sanpham')
            return HTTPFound(location=url,
                         headers=headers)

        return dict(sanpham=sanpham)
        
    @view_config(route_name='createreport', renderer='dh/createreport.pt', permission='edit')
    def createreport(self):
        request = self.request

        return {
            'status': 'Tạo báo biểu'
        }

    @view_config(route_name='create', renderer='dh/create.pt')
    def createreport(self):
        request = self.request

        if 'form.export' in request.params:
            start = request.params['from']
            end = request.params['to']

            sps = DBSession.query(ChiTietHDBH).filter(ChiTietHDBH.ngaytao.between(start, end))

                
            return dict(sps=sps, start=start, end=end)

        if 'form.import' in request.params:
            start = request.params['from']
            end = request.params['to']

            sps = DBSession.query(ChiTietHDNH).filter(ChiTietHDNH.ngaytao.between(start, end))

                
            return dict(sps=sps, start=start, end=end)

        return {
            'status': 'Tạo báo biểu'
        }


