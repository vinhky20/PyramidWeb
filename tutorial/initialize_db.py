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
        sofa = DanhMuc(id_dm=1, tendanhmuc='sofa')
        ban = DanhMuc(id_dm=2, tendanhmuc='bàn')
        tranh = DanhMuc(id_dm=3, tendanhmuc='tranh')
        guong = DanhMuc(id_dm=4, tendanhmuc='gương')

        DBSession.add(sofa)
        DBSession.add(ban)
        DBSession.add(tranh)
        DBSession.add(guong)


        test = SanPham(id_sp='test', tensanpham='test', donvitinh='test', id_dm=1)

        S1 = SanPham(id_sp='S1', tensanpham='Sofa mềm', donvitinh='bộ', id_dm=1)
        S2 = SanPham(id_sp='S2', tensanpham='Sofa dài', donvitinh='bộ', id_dm=1)

        B1 = SanPham(id_sp='B1', tensanpham='Bàn tròn', donvitinh='cái', id_dm=2)
        B2 = SanPham(id_sp='B2', tensanpham='Bàn xoay', donvitinh='cái', id_dm=2)

        T1 = SanPham(id_sp='T1', tensanpham='Tranh trừu tượng', donvitinh='bức', id_dm=3)
        T2 = SanPham(id_sp='T2', tensanpham='Tranh thiếu nữ', donvitinh='bức', id_dm=3)

        G1 = SanPham(id_sp='G1', tensanpham='Gương treo tường', donvitinh='cái', id_dm=4)

        DBSession.add(test)
        DBSession.add(S1)
        DBSession.add(S2)
        DBSession.add(T1)
        DBSession.add(T2)
        DBSession.add(B1)
        DBSession.add(B2)
        DBSession.add(G1)


        NV = NhanVien(id_nv=1, tennhanvien='Vinh Ky', username='vinhky', password='vinhky')

        DBSession.add(NV)