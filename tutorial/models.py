from pyramid.authorization import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    String,
    Date,
    func
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()

class DanhMuc(Base):
    __tablename__ = 'danhmuc'
    id_dm = Column(Integer, primary_key=True)
    tendanhmuc = Column(String(250), nullable=False)

class SanPham(Base):
    __tablename__ = 'sanpham'
    id_sp = Column(String(10), primary_key=True)
    tensanpham = Column(String(250), nullable=False)
    donvitinh = Column(String(250), nullable=False)
    id_dm = Column(Integer, ForeignKey('danhmuc.id_dm'))
    danhmuc = relationship(DanhMuc)

class NhanVien(Base):
    __tablename__ = 'nhanvien'
    id_nv = Column(Integer, primary_key=True)
    tennhanvien = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

class HoaDonBanHang(Base):
    __tablename__ = 'hoadonbanhang'
    ngaytao = Column(Date)
    id_hdbh = Column(Integer, primary_key=True)
    tenhdbh = Column(String(250), nullable=False)
    id_nv = Column(Integer, ForeignKey('nhanvien.id_nv'))
    nhanvien = relationship(NhanVien)

class ChiTietHDBH(Base):
    __tablename__ = 'chitiethdbh'
    soluong = Column(Integer)
    giasp = Column(Integer)
    id_sp = Column(String(10), ForeignKey('sanpham.id_sp'), primary_key=True)
    id_hdbh = Column(Integer, ForeignKey('hoadonbanhang.id_hdbh'), primary_key=True)
    sanpham = relationship(SanPham)
    hoadonbanhang = relationship(HoaDonBanHang)

class HoaDonNhapHang(Base):
    __tablename__ = 'hoadonnhaphang'
    ngaytao = Column(Date)
    id_hdnh = Column(Integer, primary_key=True)
    tenhdnh = Column(String(250), nullable=False)
    id_nv = Column(Integer, ForeignKey('nhanvien.id_nv'))
    nhanvien = relationship(NhanVien)

class ChiTietHDNH(Base):
    __tablename__ = 'chitiethdnh'
    soluong = Column(Integer)
    giasp = Column(Integer)
    id_sp = Column(String(10), ForeignKey('sanpham.id_sp'), primary_key=True)
    id_hdnh = Column(Integer, ForeignKey('hoadonnhaphang.id_hdnh'), primary_key=True)
    sanpham = relationship(SanPham)
    hoadonnhaphang = relationship(HoaDonNhapHang)

        