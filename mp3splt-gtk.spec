%define _legacy_common_support 1
%bcond_with audacious
%bcond_without gtk3

Summary: Gtk frontend for mp3splt
Name:    mp3splt-gtk
Version: 0.9.2
Release: 16%{?dist}
License: GPLv2
Source:  http://downloads.sourceforge.net/mp3splt/%{name}-%{version}.tar.gz
Patch0:  v0.9.2..385d2001_2020-11-10.patch
URL:     http://mp3splt.sourceforge.net/

BuildRequires: dbus-glib-devel
BuildRequires: cutter-devel
BuildRequires: libmp3splt-devel >= %{version}
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
%if %{with gtk3}
BuildRequires: gtk3-devel >= 3.0
%{?with_audacious:BuildRequires: libaudclient-devel >= 3.0}
%else
BuildRequires: gtk2-devel >= 2.18
%{?with_audacious:BuildRequires: audacious-devel < 3.0}
%endif
BuildRequires: doxygen
BuildRequires: gnome-doc-utils
BuildRequires: scrollkeeper
# Needed while using autogen.sh
BuildRequires: automake autoconf libtool gettext-devel
#dotconf-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: desktop-file-utils

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Mp3Splt-project is a utility to split mp3, ogg vorbis and native FLAC files
selecting a begin and an end time position, without decoding. It's very useful
to split large mp3/ogg vorbis/FLAC to make smaller files or to split entire
albums to obtain original tracks. If you want to split an album, you can select
split points and filenames manually or you can get them automatically from CDDB
(internet or a local file) or from .cue files. Supports also automatic silence
split, that can be used also to adjust cddb/cue splitpoints. Trimming using
silence detection is also available. You can extract tracks from Mp3Wrap or
AlbumWrap files in few seconds. For mp3 files, both ID3v1 & ID3v2 tags are
supported. Mp3splt-project is split in 3 parts : libmp3splt, mp3splt and
mp3splt-gtk. 


%prep
%setup -q
%patch0 -p2
%{_bindir}/iconv -f iso8859-1 -t utf8 AUTHORS -o AUTHORS.txt
touch -r AUTHORS AUTHORS.txt
mv AUTHORS.txt AUTHORS
#sed -i -e's,PREFIX/mp3splt-gtk_ico.svg,mp3splt-gtk_ico,g' mp3splt-gtk.desktop.in
# gtk3 is broken on F14
# sed -i -e's/gtk+-3.0 >= 3.0/gtk+-3.0 >= 2.90/g' configure.ac
# sed -i -e's/gtk+-2.0 >= 2.20/gtk+-2.0 >= 2.18/g' configure.ac
# sed -i -e's/audclient/audacious/g' configure.ac

%build
#remove old generated files
rm -f po/Makefile.in.in
rm -f build-aux/*
rm -f m4/*m4
rm -f m4/Makefile.in
rm -f libtool aclocal.m4 config.status configure autom4te.cache/* ltmain.sh
rm -f ABOUT-NLS config.h.in~ Makefile.in

autopoint
aclocal
autoheader
gnome-doc-prepare
autoconf 
libtoolize
automake --add-missing
%configure %{!?with_audacious:--disable-audacious}

%make_build

%install
%make_install
%find_lang %{name}

%check
# menu entry
desktop-file-validate %{_builddir}/%{name}-%{version}/%{name}.desktop


%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS ChangeLog README
%license COPYING
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_ico.svg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/mp3splt-gtk.*

%changelog
* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Sérgio Basto <sergio@serjux.com> - 0.9.2-15
- Update to last git snapshot from https://github.com/mp3splt/mp3splt

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 03 2019 Leigh Scott <leigh123linux@gmail.com> - 0.9.2-7
- Rebuild for new gstreamer1 version
- Remove Group tag
- Remove scriptlets

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 02 2015 Sérgio Basto <sergio@serjux.com> - 0.9.2-1
- Update to 0.9.2 .
- Disable libaudacious, use gstreamer is recommend by upstream.
- Drop BRs: libgnomeui-devel graphviz to not install gtk2.

* Fri Aug 30 2013 Paulo Roma <roma@lcg.ufrj.br> 0.9-13
- Update to 0.9

* Sun Mar 31 2013 Paulo Roma <roma@lcg.ufrj.br> 0.8.2-12
- Update to 0.8.2

* Fri Sep 07 2012 Paulo Roma <roma@lcg.ufrj.br> 0.7.3-11
- Update to 0.7.3

* Wed Jun 06 2012 Paulo Roma <roma@lcg.ufrj.br> 0.7.2-10
- Update to 0.7.2
- Removed configure.ac.patch
- Applied spinner patch for missing gtk2 functions in rhel6.

* Mon Feb 13 2012 Paulo Roma <roma@lcg.ufrj.br> 0.7.1-10
- Added -ldbus-glib-1 to LDFLAGS 
  ('dbus_g_bus_get' is defined in DSO /usr/lib64/libdbus-glib-1.so.2)

* Wed Jan 04 2012 Paulo Roma <roma@lcg.ufrj.br> 0.7.1-9
- Updated to 0.7.1
- Audacious 3 requires gtk3, and had to used autogen.sh

* Sat Sep 03 2011 Paulo Roma <roma@lcg.ufrj.br> 0.7-9
- Updated to 0.7

* Sun Mar 13 2011 Paulo Roma <roma@lcg.ufrj.br> 0.6.1a-8
- Updated to 0.6.1a
- Fixed desktop entry.
- Added BR gnome-doc-utils and scrollkeeper.
- Added in %%{_datadir}: gnome/help, omf and mp3splt-gtk.

* Mon Sep 27 2010 Paulo Roma <roma@lcg.ufrj.br> 0.6-6
- Updated to 0.6

* Mon Feb 22 2010 Paulo Roma <roma@lcg.ufrj.br> 0.5.9-6_1
- Linking with audclient.

* Wed Feb 17 2010 Paulo Roma <roma@lcg.ufrj.br> 0.5.9-6
- Updated to 0.5.9
- Using desktop-file-install.

* Wed Nov 04 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.8a-5
- Updated to 0.5.8a

* Sat Oct 31 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.8-5
- Updated to 0.5.8

* Thu Jul 30 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.7a-5
- Bugfix release: 0.5.7a

* Mon Jul 27 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.7-5
- Updated to 0.5.7

* Sat May 16 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.6-4
- Updated to 0.5.6

* Mon May 11 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.5-4
- Added BR libtool-ltdl-devel and dbus-glib-devel.

* Sat May 09 2009 Paulo Roma <roma@lcg.ufrj.br> 0.5.5-3
- Updated to 0.5.5

* Sun Mar 22 2009 Paulo Roma <roma@lcg.ufrj.br> 0.3.1-2
- Using find_lang.
- Converted AUTHORS to utf8.

* Sun Aug 26 2007 Paulo Roma <roma@lcg.ufrj.br> 0.3.1-1
- Initial spec file.
