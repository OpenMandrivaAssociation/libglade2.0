# enable_gtkdoc: whether gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define enable_gtkdoc 1

# End of user configurable section

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}

%define req_libxml2_version	2.4.10
%define req_atk_version		1.9.0
%define req_gtk_version		2.5.0

%define pkgname		libglade
%define api_version	2.0
%define lib_major	0
%define lib_name	%mklibname glade %{api_version} %{lib_major}

Summary:	Library for dynamically loading GLADE interface files
Name:		%{pkgname}%{api_version}
Version: 2.6.2
Release: %mkrel 1
License:	LGPL
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# (fc) 2.5.1-3mdk fix some warnings (Fedora) (GNOME bug #121025)
Patch0:		libglade-2.0.1-nowarning.patch
BuildRoot:	%{_tmppath}/%{pkgname}-%{version}-buildroot

BuildConflicts:	libglade0-devel < 0.17

BuildRequires:	autoconf2.5
BuildRequires:	libxml2-devel >= %{req_libxml2_version}
BuildRequires:	libatk1.0-devel >= %{req_atk_version}
BuildRequires:	libgtk+2.0-devel >= %{req_gtk_version}
BuildRequires:	libglib2.0-devel >= 2.3.1
BuildRequires:	python >= 2.0
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif

%description
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.


%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Provides:	%{pkgname}%{api_version} = %{version}-%{release}
Requires:	libxml2 >= %{req_libxml2_version}

%description -n %{lib_name}
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.


%package -n %{lib_name}-devel
Summary:	Libraries, includes, etc to develop libglade applications
Group:		Development/GNOME and GTK+
Conflicts:	libglade0-devel < 0.17
Provides:	%{pkgname}%{api_version}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:	libgtk+2.0-devel >= %{req_gtk_version}
Requires:	libxml2-devel >= %{req_libxml2_version}
# $bindir/libglade-convert is python script
Requires:	python >= 2.0
Requires(post):     sgml-common >= 0.6.3-2mdk
Requires(postun):     sgml-common >= 0.6.3-2mdk


%description -n %{lib_name}-devel
%{pkgname} allows you to load user interfaces in your program, which are
stored externally.  This allows alteration of the interface without
recompilation of the program.

This package contains static libraries, include files, etc so that
you can use to develop %{pkgname} applications.


%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .warnings

%build
%configure2_5x \
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

%clean
rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
CATALOG=/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add "system" \
		"http://glade.gnome.org/glade-2.0.dtd" \
		%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true

%postun -n %{lib_name}-devel
# Do not remove if upgrade
if [ "$1" = "0" ]; then
 CATALOG=/etc/xml/catalog
 if [ -f $CATALOG -a -x %{_bindir}/xmlcatalog ]; then 
  %{_bindir}/xmlcatalog --noout --del \
         	%{_datadir}/xml/libglade/glade-2.0.dtd $CATALOG || true
 fi
fi

%files -n %{lib_name}
%defattr(-, root, root)
%doc README ChangeLog
%{_libdir}/lib*.so.*
%dir %{_libdir}/libglade
%dir %{_libdir}/libglade/%{api_version}

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc AUTHORS examples
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/*
%{_datadir}/xml/libglade
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*


