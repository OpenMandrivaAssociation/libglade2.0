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
Release: 	9
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# (fc) 2.5.1-3mdk fix some warnings (Fedora) (GNOME bug #121025)
Patch0:		libglade-2.0.1-nowarning.patch
Patch1:		libglade-2.6.4-linkage.patch

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
Obsoletes:	%{mklibname glade 2.0 0}-devel < 2.6.4-9

%description -n %{develname}
This package contains libraries, include files, etc so that
you can use to develop %{pkgname} applications.


%prep
%setup -q -n %{pkgname}-%{version}
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
mkdir -p %{buildroot}%{_libdir}/libglade/%{api_version}

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



%changelog
* Wed Nov 16 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.6.4-8
+ Revision: 730809
- rebuild
  cleaned up spec
  removed defattr
  removed old ldconfig scriptlets
  removed clean section
  switched to apply_patches macro
  removed reqs for devel pkgs in the devel pkg
  removed unneeded virtual provide
  removed old conflicts & buildconflicts
  converted BRs to pkgconfig provides
  remove mkrel macro

* Mon Sep 19 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.4-7
+ Revision: 700324
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.6.4-6
+ Revision: 662372
- mass rebuild

* Tue Mar 22 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.6.4-5
+ Revision: 647481
- adjusted BuildRequires
- fixed configure
- made more proper the Obsoletes
- dropped major from devel pkg
- disabled static build
- cleaned up devel description

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 2.6.4-4mdv2011.0
+ Revision: 602551
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.6.4-3mdv2010.1
+ Revision: 520826
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.6.4-2mdv2010.0
+ Revision: 425548
- rebuild

* Tue Mar 17 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.4-1mdv2009.1
+ Revision: 356642
- update to new version 2.6.4

* Tue Aug 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.3-1mdv2009.0
+ Revision: 273545
- new version
- drop patch 1
- update license

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.6.2-7mdv2009.0
+ Revision: 222595
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 26 2008 Emmanuel Andry <eandry@mandriva.org> 2.6.2-6mdv2008.1
+ Revision: 190525
- Fix lib group

* Thu Feb 21 2008 Frederic Crozat <fcrozat@mandriva.com> 2.6.2-5mdv2008.1
+ Revision: 173657
- Patch1 (SVN): fix invalmid call to g_free

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 21 2007 David Walluck <walluck@mandriva.org> 2.6.2-3mdv2008.0
+ Revision: 92091
- add devel provides for fc compat

* Wed Aug 15 2007 Adam Williamson <awilliamson@mandriva.org> 2.6.2-2mdv2008.0
+ Revision: 63596
- fix autoconf buildrequires
- drop manual dependency on libxml2, it has an auto-generated one anyway

* Tue Jul 31 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.2-1mdv2008.0
+ Revision: 56919
- new version

* Tue Jun 19 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.1-1mdv2008.0
+ Revision: 41348
- new version


* Thu Nov 30 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.0-2mdv2007.0
+ Revision: 88961
- Import libglade2.0

* Thu Nov 30 2006 Götz Waschk <waschk@mandriva.org> 2.6.0-2mdv2007.1
- unpack patch

* Thu Jul 13 2006 Götz Waschk <waschk@mandriva.org> 2.6.0-1mdv2007.0
- drop patch 1
- New release 2.6.0

* Sat Apr 15 2006 Frederic Crozat <fcrozat@mandriva.com> 2.5.1-3mdk
- Patch0 (Fedora): fix some warnings (GNOME bug #121025)
- Patch1 (CVS): make non-ASCII invisible characters work (GNOME bug #321119)

* Wed Oct 12 2005 Frederic Crozat <fcrozat@mandriva.com> 2.5.1-2mdk
- replace prereq with new syntax
- Rebuild to get debug package

* Wed Apr 20 2005 Frederic Crozat <fcrozat@mandriva.com> 2.5.1-1mdk 
- Release 2.5.1 (based on Götz Waschk package)

* Sat Feb 12 2005 Götz Waschk <waschk@linux-mandrake.com> 2.4.2-1mdk
- drop merged patch
- New release 2.4.2

* Fri Feb 11 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.1-2mdk 
- Patch0 (CVS): fix regressions (Mdk bug #12574)

* Mon Nov 29 2004 Götz Waschk <waschk@linux-mandrake.com> 2.4.1-1mdk
- reenable libtoolize
- drop patch
- New release 2.4.1

* Fri Sep 24 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.0-2mdk
- Patch0 (CVS): fix accelerator not set when using stock entries

* Tue May 18 2004 Götz Waschk <waschk@linux-mandrake.com> 2.4.0-1mdk
- fix source URL
- New release 2.4.0

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.3.6-1mdk
- Release 2.3.6 (with Götz Waschk help)
- requires new glib2
- fix doc list
- requires new gtk
- don't run libtoolize
- don't regenerate the auto* stuff

