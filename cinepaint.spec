%define major 	  0
%define	libname   %mklibname cinepaint %{major}
%define develname %mklibname -d cinepaint
%define minor 	  0
%define revision  22

%define ver	%{major}.%{revision}
%define rel	%mkrel 4
%define subver 1

%define use_gutenprint	0
%{?_with_print: %global use_gutenprint 1}
%{?_without_print: %global use_gutenprint 0}

Summary:       A tool for manipulating high-colordepth images
Name:          cinepaint
Version:       %ver
Release:       %rel
License:       GPL
Group:         Graphics
URL:           http://www.cinepaint.org
Source0:       http://downloads.sourceforge.net/cinepaint/cinepaint-%{version}-%{subver}.tar.gz
Source1:       icons-%{name}.tar.bz2
Patch2:        cinepaint-0.22-openexr.patch
Patch4:        cinepaint-0.21-python.patch
Patch5:        cinepaint-0.21-python64.patch
Patch6: 	cinepaint-0.22-0-icc_helfer_fltk.patch
Patch8:         cinepaint-0.22-gcc43_cine.patch
BuildRequires: bison
BuildRequires: desktop-file-utils
BuildRequires: GL-devel
BuildRequires: flex
BuildRequires: fltk-devel
BuildRequires: python-devel
BuildRequires: libgtk+-devel >= 1.2.8
BuildRequires: libgtk+2-devel
BuildRequires: libjpeg-devel
BuildRequires: lcms-devel
BuildRequires: libmesaglu-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libgimp-devel
BuildRequires: libxmu-devel
BuildRequires: libxpm-devel
BuildRequires: OpenEXR-devel
BuildRequires: libOpenEXR-devel
BuildRequires: gutenprint-devel >= 5.0.0-0.8mdk
%if %{use_gutenprint}
BuildRequires: libgutenprintui2-devel >= 5.0.0-0.8mdk
%endif
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Obsoletes:     filmgimp
Provides:      filmgimp
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
CinePaint is a free open source painting and image retouching program
designed to work best with 35mm film and other high resolution high
dynamic range images. 

The 32-bit per channel color range of CinePaint appeals to 35mm
cinematographers and professional still photographers because film
scanners are capable of greater color bit-depth than can be displayed
on an 8-bit per channel monitor or can be manipulated in typical
programs. However, CinePaint is a general-purpose tool useful for
working on images for motion pictures, print, and the Web. CinePaint
supports many file formats, both conventional formats such as JPEG,
PNG, TIFF, and TGA images -- and more exotic cinema formats such as
Cineon and OpenEXR.


%package -n %{libname}
Summary:	CinePaint libraries
Group:		System/Libraries
License:	GPL
Provides:	libcinepaint = %version-%release

%description -n %{libname}
This package contains shared libraries used by CinePaint.

%package -n %{develname}
Summary:	CinePaint plugins and extension development kit
Group:		Development/C
Requires:	%{libname} = %version
Provides:	cinepaint-devel
Provides:	libcinepaint-devel = %version-%release
Obsoletes:	%mklibname cinepaint 0 -d

%description -n %{develname}
Static libraries and header files for writing CinePaint plugins and
extensions.

%prep

%setup -q -n %{name}-%{version}-%{subver}
%patch2 -p1 -b .openexr
%patch4 -p1 -b .python
%ifarch x86_64
%patch5 -p1 -b .python64
%endif
%patch6 -p1
%patch8 -p1 -b .gcc43_cine

aclocal && autoconf && automake
chmod +x ./mkinstalldirs

%build
%configure2_5x \
%if %use_gutenprint
	--enable-print \
%else
	--disable-print \
%endif
	--enable-gtk2 \
	--enable-pygimp
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std


mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
tar -xjf %{SOURCE1} -C $RPM_BUILD_ROOT%{_iconsdir}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Graphics" \
  --add-category="RasterGraphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root,0755)
%dir %{_datadir}/cinepaint
%dir %{_datadir}/cinepaint/%{ver}-%{subver}
%dir %{_libdir}/cinepaint
%dir %{_libdir}/cinepaint/%{ver}-%{subver}
%{_bindir}/cinepaint
%{_bindir}/cinepaint-remote
%{_mandir}/man1/cinepaint.1*
%{_libdir}/cinepaint/%{ver}-%{subver}/*
%{_datadir}/cinepaint/%{ver}-%{subver}/*
%{_datadir}/fonts/FreeSans.ttf
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{py_puresitedir}/*
%{py_platsitedir}/*

%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/libcinepaint*.so.*

%files -n %{develname}
%defattr(-,root,root,0755)
%{_bindir}/cinepainttool
%{_datadir}/aclocal/cinepaint.m4
%{_includedir}/*
%{_mandir}/man1/cinepainttool.1*
%{_libdir}/*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*
%attr(0644,root,root) %{_libdir}/lib*.la
