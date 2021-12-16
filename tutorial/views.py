import colander
import datetime
import transaction
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
)

from sqlalchemy import (
    func
)

from pyramid.view import (
    view_config,
    view_defaults
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

from .models import DBSession, SanPham, NhanVien, DanhMuc, ChiTietHDBH, ChiTietHDNH, HoaDonBanHang, HoaDonNhapHang


@view_defaults(renderer='home.pt')
class Home:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home')
    def home(self):
                
        return {'name': 'Nội Thất Sweet Home'}
            

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

        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user = USERS.get(login)

            if (user == password):
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
            transaction.commit()


            # XOÁ USERNAME CŨ SAU KHI CẬP NHẬT THÔNG TIN TÀI KHOẢN
            USERS.pop(un)

            
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

class ManageCategory:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='danhmuc', renderer='dm/danhmuc.pt', permission='edit')
    def showdanhmuc(self):
        request = self.request
        danhmucs = DBSession.query(DanhMuc)

        if 'form.delete' in request.params:
            id_dm = request.params['id_dm']

            DBSession.query(DanhMuc).filter_by(id_dm=id_dm).delete()

        if 'form.add' in request.params:
            id_dm = request.params['id_dm']
            tendanhmuc = request.params['tendanhmuc']

            DBSession.add(DanhMuc(id_dm=id_dm, tendanhmuc=tendanhmuc))
            
        return dict(danhmucs=danhmucs)


    @view_config(route_name='updatedm', renderer='dm/updatedm.pt', permission='edit')
    def updateDM(self):
        request = self.request
        id_dm = str(self.request.matchdict['id_dm'])
        danhmuc = DBSession.query(DanhMuc).filter_by(id_dm=id_dm).one()

        if 'form.update' in request.params:
            tendanhmuc = request.params['tendanhmuc']

            danhmuc.tendanhmuc = tendanhmuc

        return dict(danhmuc=danhmuc)

class ManageProduct:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='search', renderer='sp/search.pt', permission='edit')
    def search(self):
        request = self.request

        

        if 'form.search' in request.params:
            kw = request.params['kw']

            search = "%{}%".format(kw)

            danhmucs = DBSession.query(DanhMuc)

            sanphams = DBSession.query(SanPham).filter(SanPham.tensanpham.like(search)).all()

            return dict(sanphams=sanphams, danhmucs=danhmucs)

        return {
            'name': 'Tìm kiếm sản phẩm'
        }

    @view_config(route_name='sanpham', renderer='sp/sanpham.pt', permission='edit')
    def showsanpham(self):
        request = self.request
        sanphams = DBSession.query(SanPham)

        danhmucs = DBSession.query(DanhMuc)

        if 'form.delete' in request.params:
            id_sp = request.params['id_sp']

            DBSession.query(SanPham).filter_by(id_sp=id_sp).delete()
            
        return dict(sanphams=sanphams, danhmucs=danhmucs)

    @view_config(route_name='sanphamtheodanhmuc', renderer='sp/sanphamtheodanhmuc.pt', permission='edit')
    def sanphamtheodm(self):
        request = self.request
        danhmucs = DBSession.query(DanhMuc)

        id_dm = self.request.matchdict['id_dm']

        sanphams = DBSession.query(SanPham).filter_by(id_dm=id_dm)

        dm = DBSession.query(DanhMuc).filter_by(id_dm=id_dm).one()

            
        return dict(sanphams=sanphams, danhmucs=danhmucs, dm=dm)


    @view_config(route_name='addsanpham', renderer='sp/addsanpham.pt', permission='edit')
    def addsanpham(self):
        request = self.request
        danhmucs = DBSession.query(DanhMuc)

        if 'form.add' in request.params:
            id_sp = request.params['masp']
            tensanpham = request.params['tensp']
            dvt = request.params['dvt']
            danhmuc = request.params['danhmuc']

            dm = DBSession.query(DanhMuc).filter_by(tendanhmuc=danhmuc).one()
            id_dm = dm.id_dm

            DBSession.add(SanPham(id_sp=id_sp, tensanpham=tensanpham, donvitinh=dvt, id_dm=id_dm))

            url = request.route_url('sanpham')
            return HTTPFound(location=url)
            
        return dict(danhmucs=danhmucs)


    @view_config(route_name='updatesp', renderer='sp/updatesp.pt', permission='edit')
    def updatesp(self):
        request = self.request
        id_sp = str(self.request.matchdict['id_sp'])
        sanpham = DBSession.query(SanPham).filter_by(id_sp=id_sp).one()
        danhmucs = DBSession.query(DanhMuc)

        if 'form.update' in request.params:
            tensanpham = request.params['tensp']
            dvt = request.params['dvt']
            danhmuc = request.params['danhmuc']

            dm = DBSession.query(DanhMuc).filter_by(tendanhmuc=danhmuc).one()
            sanpham.tensanpham = tensanpham
            sanpham.donvitinh = dvt
            sanpham.id_dm = dm.id_dm


        return dict(sanpham=sanpham, danhmucs=danhmucs)
        
    @view_config(route_name='createreport', renderer='dh/createreport.pt', permission='edit')
    def createreport(self):
        request = self.request

        return {
            'status': 'Tạo báo biểu'
        }

    @view_config(route_name='createBBHDBH', renderer='dh/createBBHDBH.pt')
    def createBBHDBH(self):
        request = self.request

        if 'form.export' in request.params:
            tenbaobieu = {
                'ten': 'được bán'
            }
            start = request.params['from']
            end = request.params['to']

            bh = DBSession.query(ChiTietHDBH, HoaDonBanHang, func.sum(ChiTietHDBH.soluong).label('totalBH')).join(HoaDonBanHang, HoaDonBanHang.id_hdbh==ChiTietHDBH.id_hdbh).filter(HoaDonBanHang.ngaytao.between(start, end)).group_by(ChiTietHDBH.id_sp)
            
            nh = DBSession.query(ChiTietHDNH, HoaDonNhapHang, func.sum(ChiTietHDNH.soluong).label('totalNH')).join(HoaDonNhapHang, HoaDonNhapHang.id_hdnh==ChiTietHDNH.id_hdnh).group_by(ChiTietHDNH.id_sp)
            BH = DBSession.query(ChiTietHDBH, HoaDonBanHang, func.sum(ChiTietHDBH.soluong).label('totalBH')).join(HoaDonBanHang, HoaDonBanHang.id_hdbh==ChiTietHDBH.id_hdbh).group_by(ChiTietHDBH.id_sp)


            A = {}
            for i in BH:
                obj = {
                    i.ChiTietHDBH.sanpham.tensanpham: int(i.totalBH)
                }
                A.update(obj)

            B = {}
            for j in nh:
                obj1 = {
                    j.ChiTietHDNH.sanpham.tensanpham: int(j.totalNH)
                }
                B.update(obj1) 


            arr = []
            for x in A:
                for y in B:
                    if x == y:
                        obj2 = {
                            'name': x,
                            'inventory': int(B[x] - A[x])
                        }

                        arr.append(obj2)
  

               
            return dict(start=start, end=end, tenbaobieu=tenbaobieu, bh=bh, arr=arr)


        return {
            'status': 'Tạo báo biểu bán hàng'
        }

    @view_config(route_name='createBBHDNH', renderer='dh/createBBHDNH.pt')
    def createBBHDNH(self):
        request = self.request

        if 'form.import' in request.params:
            tenbaobieu = {
                'ten': 'được nhập'
            }
            start = request.params['from']
            end = request.params['to']

            sps = DBSession.query(ChiTietHDNH, HoaDonNhapHang, func.sum(ChiTietHDNH.soluong).label('totalNH')).join(HoaDonNhapHang, HoaDonNhapHang.id_hdnh==ChiTietHDNH.id_hdnh).filter(HoaDonNhapHang.ngaytao.between(start, end)).group_by(ChiTietHDNH.id_sp)
                
            nhs = DBSession.query(ChiTietHDNH, HoaDonNhapHang, func.sum(ChiTietHDNH.soluong).label('totalNH')).join(HoaDonNhapHang, HoaDonNhapHang.id_hdnh==ChiTietHDNH.id_hdnh).group_by(ChiTietHDNH.id_sp)

            return dict(sps=sps, start=start, end=end, tenbaobieu=tenbaobieu, nhs=nhs)



        return {
            'status': 'Tạo báo biểu nhập'
        }
    
    @view_config(route_name='create-bill', renderer='dh/bill.pt', permission='edit')
    def createBill(self):
        request = self.request

        tennv = request.authenticated_userid

        nv = DBSession.query(NhanVien).filter_by(username=tennv).one()

        if 'form.hdbh' in request.params:
            tenhdbh = request.params['tenhd']
            DBSession.add(HoaDonBanHang(ngaytao=datetime.date.today(), tenhdbh=tenhdbh, id_nv=nv.id_nv))

            hdbh = DBSession.query(HoaDonBanHang).filter_by(tenhdbh=tenhdbh).one()
            id_hdbh = hdbh.id_hdbh

            DBSession.add(ChiTietHDBH(id_hdbh=id_hdbh, id_sp='test', soluong=0, giasp=50000))


        if 'form.hdnh' in request.params:
            tenhdnh = request.params['tenhd']
            DBSession.add(HoaDonNhapHang(ngaytao=datetime.date.today(), tenhdnh=tenhdnh, id_nv=nv.id_nv))

            hdnh = DBSession.query(HoaDonNhapHang).filter_by(tenhdnh=tenhdnh).one()
            id_hdnh = hdnh.id_hdnh

            DBSession.add(ChiTietHDNH(id_hdnh=id_hdnh, id_sp='test', soluong=0, giasp=50000))


        if 'form.delete.hdbh' in request.params:
            idhdbh = request.params['id']
            DBSession.query(ChiTietHDBH).filter_by(id_hdbh=idhdbh).delete()
            DBSession.query(HoaDonBanHang).filter_by(id_hdbh=idhdbh).delete()

        if 'form.delete.hdnh' in request.params:
            idhdnh = request.params['id']
            DBSession.query(ChiTietHDNH).filter_by(id_hdnh=idhdnh).delete()
            DBSession.query(HoaDonNhapHang).filter_by(id_hdnh=idhdnh).delete()


        bhs = DBSession.query(HoaDonBanHang)
        nhs = DBSession.query(HoaDonNhapHang)

        return dict(bhs=bhs, nhs=nhs)

    @view_config(route_name='create-hdbh', renderer='dh/hdbh.pt', permission='edit')
    def createHDBH(self):
        request = self.request
        id_hdbh = int(self.request.matchdict['id_hdbh'])

        idhdbh = {
            'id_hdbh': id_hdbh
        }

        NV = DBSession.query(HoaDonBanHang).filter_by(id_hdbh=id_hdbh).one()

        idNV = NV.id_nv

        tenNV = DBSession.query(NhanVien).filter_by(id_nv=idNV).one()

        tennhanvien = tenNV.tennhanvien

        ten = {
            'tenNV': tennhanvien
        }

        ngaytaohd = datetime.date.today()

        tenhd = DBSession.query(HoaDonBanHang).filter_by(id_hdbh=id_hdbh).one()

        cts = DBSession.query(ChiTietHDBH).filter_by(id_hdbh=id_hdbh)

        if 'form.addToBill' in request.params:
            id_sp = request.params['masp']
            soluong = request.params['soluong']
            giasp = request.params['giasp']

            DBSession.add(ChiTietHDBH(id_hdbh=id_hdbh, id_sp=id_sp, soluong=soluong, giasp=giasp))
            DBSession.query(ChiTietHDBH).filter_by(id_sp='test', id_hdbh=id_hdbh).delete()

        totalProduct = {}
        total = []
        e = {}
        for ct in cts:
            e[ct.id_sp] = ct.soluong * ct.giasp
            x = ct.soluong * ct.giasp
            total.append(x)
        totalProduct.update(e)

        totalBill = 0

        for i in total:
            totalBill+=i

        if 'form.submit' in request.params:
            DBSession.query(ChiTietHDBH).filter_by(id_sp='test', id_hdbh=id_hdbh).delete()
            url = request.route_url('create-bill')
            return HTTPFound(location=url)

        if 'form.delete' in request.params:
            DBSession.query(ChiTietHDBH).filter_by(id_hdbh=id_hdbh).delete()
            DBSession.query(HoaDonBanHang).filter_by(id_hdbh=id_hdbh).delete()
            
            url = request.route_url('create-bill')
            return HTTPFound(location=url)

        if 'form.deleteSP' in request.params:
            id_sp = request.params['id_sp']
            gia = request.params['gia']
            totalBill = totalBill - int(gia)
            DBSession.query(ChiTietHDBH).filter_by(id_sp=id_sp, id_hdbh=id_hdbh).delete()
            

        return dict(cts=cts, idhdbh=idhdbh, ngaytaohd=ngaytaohd, totalProduct=totalProduct, ten=ten, totalBill=totalBill, tenhd=tenhd)


    @view_config(route_name='create-hdnh', renderer='dh/hdnh.pt', permission='edit')
    def createHDNH(self):
        request = self.request
        id_hdnh = int(self.request.matchdict['id_hdnh'])

        idhdnh = {
            'id_hdnh': id_hdnh
        }

        NV = DBSession.query(HoaDonNhapHang).filter_by(id_hdnh=id_hdnh).one()

        idNV = NV.id_nv

        tenNV = DBSession.query(NhanVien).filter_by(id_nv=idNV).one()

        tennhanvien = tenNV.tennhanvien

        ten = {
            'tenNV': tennhanvien
        }

        ngaytaohd = datetime.date.today()

        cts = DBSession.query(ChiTietHDNH).filter_by(id_hdnh=id_hdnh)

        tenhd = DBSession.query(HoaDonNhapHang).filter_by(id_hdnh=id_hdnh).one()

        if 'form.addToBill' in request.params:
            id_sp = request.params['masp']
            soluong = request.params['soluong']
            giasp = request.params['giasp']

            DBSession.add(ChiTietHDNH(id_hdnh=id_hdnh, id_sp=id_sp, soluong=soluong, giasp=giasp))
            DBSession.query(ChiTietHDNH).filter_by(id_sp='test', id_hdnh=id_hdnh).delete()

        totalProduct = {}
        total = []
        e = {}
        for ct in cts:
            e[ct.id_sp] = ct.soluong * ct.giasp
            x = ct.soluong * ct.giasp
            total.append(x)
        totalProduct.update(e)

        totalBill = 0

        for i in total:
            totalBill+=i

        if 'form.submit' in request.params:
            DBSession.query(ChiTietHDNH).filter_by(id_sp='test', id_hdnh=id_hdnh).delete()

            url = request.route_url('create-bill')
            return HTTPFound(location=url)

        if 'form.delete' in request.params:
            DBSession.query(ChiTietHDNH).filter_by(id_hdnh=id_hdnh).delete()
            DBSession.query(HoaDonNhapHang).filter_by(id_hdnh=id_hdnh).delete()

            url = request.route_url('create-bill')
            return HTTPFound(location=url)

        if 'form.deleteSP' in request.params:
            id_sp = request.params['id_sp']
            gia = request.params['gia']
            totalBill = totalBill - int(gia)
            DBSession.query(ChiTietHDNH).filter_by(id_sp=id_sp, id_hdnh=id_hdnh).delete()
            

        return dict(cts=cts, idhdnh=idhdnh, ngaytaohd=ngaytaohd, totalProduct=totalProduct, ten=ten, totalBill=totalBill, tenhd=tenhd)

