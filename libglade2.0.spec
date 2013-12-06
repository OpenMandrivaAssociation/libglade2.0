%define url_ver %(echo %{version}|cut -d. -f1,2)

%define enable_gtkdoc 1
%define pkgname	libglade
%define api	2.0
%define major	0
%define libname	%mklibname glade %{api} %{major}
%define devname	%mklibname glade %{api} -d

Summary:	Library for dynamically loading GLADE interface files
Name:		%{pkgname}%{api}
Version: 	2.6.4
Release: 	17
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libglade/%{url_ver}/%{pkgname}-%{version}.tar.bz2
# (fc) 2.5.1-3mdk fix some warnings (Fedora) (GNOME bug #121025)
Patch0:		libglade-2.0.1-nowarning.patch
Patch1:		libglade-2.6.4-linkage.patch

%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
BuildRequires:	python >= 2.0
BuildRequires:	pkgconfig(atk) >= 1.9.0
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.5.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.3.1
BuildRequires:	pkgconfig(libxml-2.0) >= 2.4.10

%description
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.

%package -n %{libname}
Summary:	%{summary}
Group:		%{group}
Provides:	%{pkgname}%{api} = %{version}-%{release}

%description -n %{libname}
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.

%package -n %{devname}
Summary:	Libraries, includes, etc to develop libglade applications
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
# $bindir/libglade-convert is python script
Requires:	python
Requires(post,postun): sgml-common >= 0.6.3-2
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname glade 2.0 0}-devel < 2.6.4-9

%description -n %{devname}
This package contains libraries, include files, etc so that
you can use to develop %{pkgname} applications.

%prep
%setup -qn %{pkgname}-%{version}
%apply_patches

%build
autoconf
%configure2_5x \
	--disable-static \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%install
%makeinstall_std

# install test program
sh ./libtool --mode=install %{_bindir}/install test-libglade %{buildroot}%{_bindir}/test-libglade

# Make libglade own %{_libdir}/libglade
mkdir -p %{buildroot}%{_libdir}/libglade/%{api}

%post -n %{devname}
CATALOG=/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add "system" \
	"http://glade.gnome.org/glade-2.0.dtd" \
	%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true

%postun -n %{devname}
# Do not remove if upgrade
if [ "$1" = "0" ]; then
 CATALOG=/etc/xml/catalog
 if [ -f $CATALOG -a -x %{_bindir}/xmlcatalog ]; then 
  %{_bindir}/xmlcatalog --noout --del \
         	%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true
 fi
fi

%files -n %{libname}
%{_libdir}/libglade-%{api}.so.%{major}*
%dir %{_libdir}/libglade
%dir %{_libdir}/libglade/%{api}

%files -n %{devname}
%doc AUTHORS examples README ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/*
%{_datadir}/xml/libglade
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

