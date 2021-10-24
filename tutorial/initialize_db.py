import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from .models import (
    DBSession,
    DanhMuc,
    SanPham,
    NhanVien,
    HoaDonBanHang,
    ChiTietHDBH,
    HoaDonNhapHang,
    ChiTietHDNH,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        modelDM = DanhMuc(id_dm=1, tendanhmuc='sofa')

        modelSP = SanPham(id_sp=1, tensanpham='Sofa siu cap vip pro', donvitinh='VND', id_dm=1)

        modelNV = NhanVien(id_nv=1, tennhanvien='Vinh Ky', username='vinhkyne', password='vinhkyne')


        DBSession.add(modelDM)
        DBSession.add(modelSP)
        DBSession.add(modelNV)