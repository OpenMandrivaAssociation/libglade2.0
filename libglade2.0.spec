# enable_gtkdoc: whether gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define enable_gtkdoc 1

# End of user configurable section

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}

%define pkgname		libglade
%define api_version	2.0
%define api_major_version 2
%define lib_major	0
%define lib_name	%mklibname glade %{api_version} %{lib_major}
%define develname	%mklibname glade %{api_version} -d

Summary:	Library for dynamically loading GLADE interface files
Name:		%{pkgname}%{api_version}
Version: 	2.6.4
Release: 	8
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# (fc) 2.5.1-3mdk fix some warnings (Fedora) (GNOME bug #121025)
Patch0:		libglade-2.0.1-nowarning.patch

%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
BuildRequires:	python >= 2.0
BuildRequires:	pkgconfig(libxml-2.0) >= 2.4.10
BuildRequires:	pkgconfig(atk) >= 1.9.0
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.5.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.3.1

%description
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.


%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Provides:	%{pkgname}%{api_version} = %{version}-%{release}

%description -n %{lib_name}
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.


%package -n %{develname}
Summary:	Libraries, includes, etc to develop libglade applications
Group:		Development/GNOME and GTK+
Requires:	%{lib_name} = %{version}-%{release}
# $bindir/libglade-convert is python script
Requires:	python
Requires(post,postun): sgml-common >= 0.6.3-2
Provides:	%{pkgname}%{api_version}-devel = %{version}-%{release}
Obsoletes:	%{mklibname glade 2.0 0}-devel 

%description -n %{develname}
This package contains libraries, include files, etc so that
you can use to develop %{pkgname} applications.


%prep
%setup -q -n %{pkgname}-%{version}
%apply_patches

%build
%configure2_5x \
	--disable-static \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# install test program
sh ./libtool --mode=install %{_bindir}/install test-libglade %{buildroot}%{_bindir}/test-libglade

# Make libglade own %{_libdir}/libglade
mkdir -p %{buildroot}%{_libdir}/libglade/%{api_version}

# remove unpackaged files
find %{buildroot} -name *.la | xargs rm

%post -n %{develname}
CATALOG=/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add "system" \
		"http://glade.gnome.org/glade-2.0.dtd" \
		%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true

%postun -n %{develname}
# Do not remove if upgrade
if [ "$1" = "0" ]; then
 CATALOG=/etc/xml/catalog
 if [ -f $CATALOG -a -x %{_bindir}/xmlcatalog ]; then 
  %{_bindir}/xmlcatalog --noout --del \
         	%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true
 fi
fi

%files -n %{lib_name}
%doc README ChangeLog
%{_libdir}/lib*.so.%{lib_major}*
%dir %{_libdir}/libglade
%dir %{_libdir}/libglade/%{api_version}

%files -n %{develname}
%doc AUTHORS examples
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/*
%{_datadir}/xml/libglade
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

