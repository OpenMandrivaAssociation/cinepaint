%define major 0
%define	libname %mklibname cinepaint %{major}
%define develname %mklibname -d cinepaint
%define minor 0
%define revision 22

%define ver	%{major}.%{revision}

%define subver 1

%define use_gutenprint	0
%{?_with_print: %global use_gutenprint 1}
%{?_without_print: %global use_gutenprint 0}

Summary:	A tool for manipulating high-colordepth images
Name:		cinepaint
Version:	%{ver}
Release:	%mkrel 8
License:	GPL
Group:		Graphics
URL:		http://www.cinepaint.org
Source0:	http://downloads.sourceforge.net/cinepaint/cinepaint-%{version}-%{subver}.tar.gz
Source1:	icons-%{name}.tar.bz2
Patch2:		cinepaint-0.22-openexr.patch
Patch4:		cinepaint-0.21-python.patch
Patch5:		cinepaint-0.21-python64.patch
Patch6: 	cinepaint-0.22-0-icc_helfer_fltk.patch
Patch8:		cinepaint-0.22.1-gcc43.patch
Patch9:		cinepaint-0.22.1-implicitdecls.patch
Patch10:	cinepaint-0.22.1-multiple_parameters_named.patch
Patch11:	cinepaint-0.22.1-rpath.patch
Patch12:	cinepaint-0.22-0-pc_req.patch
Patch13:	cinepaint-0.22-0-libdir.patch
Patch14:	cinepaint-0.22-1-linkage_fix.diff
Patch15:	cinepaint-0.22.1-fix-str-fmt.patch
Patch16:	cinepaint-0.22.1-new-fltk.patch
Patch17:	cinepaint-0.22-gcc44.patch
BuildRequires:	bison
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	GL-devel
BuildRequires:	gutenprint-devel >= 5.0.0-0.8mdk
BuildRequires:	lcms-devel
BuildRequires:	libgimp-devel
BuildRequires:	libgtk+2-devel
BuildRequires:	libgtk+-devel >= 1.2.8
BuildRequires:	libjpeg-devel
BuildRequires:	libmesaglu-devel
BuildRequires:	libOpenEXR-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxpm-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	python-devel
%if %{use_gutenprint}
BuildRequires:	libgutenprintui2-devel >= 5.0.0-0.8mdk
%endif
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Obsoletes:	filmgimp
Provides:	filmgimp
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

%package -n	%{libname}
Summary:	CinePaint libraries
Group:		System/Libraries
License:	GPL
Provides:	libcinepaint = %{version}-%{release}

%description -n	%{libname}
This package contains shared libraries used by CinePaint.

%package -n	%{develname}
Summary:	CinePaint plugins and extension development kit
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	cinepaint-devel
Provides:	libcinepaint-devel = %{version}-%{release}
Obsoletes:	%{mklibname cinepaint 0 -d}

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
%patch8 -p1 -b .gcc43
%patch9 -p1 -b .implicitdecls
%patch10 -p1 -b .multiple_parameters_named
%patch11 -p1 -b .rpath
%patch12 -p1 -b .req
%patch13 -p1 -b .libdir
%patch14 -p1 -b .linkage_fix
%patch15 -p0 -b .str
%patch16 -p0 -b .fltk
%patch17 -p1 -b .gcc44

%build
libtoolize --copy --force
aclocal
autoconf
automake
chmod +x ./mkinstalldirs

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
rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}%{_iconsdir}
tar -xjf %{SOURCE1} -C %{buildroot}%{_iconsdir}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Graphics" \
  --add-category="RasterGraphics" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name} --all-name

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

%clean
rm -rf %{buildroot}

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
%{_libdir}/libcinepaint*.so.%{major}*

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
