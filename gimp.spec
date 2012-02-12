#### options:
# Use the following --with/--without <option> switches to control how the
# package will be built:
# 
# lcms:        lcms support
%bcond_without lcms
# python:      python support
%bcond_without python
# mp:          multi processor support
%bcond_without mp
# static:      build static libraries
%bcond_with static
# print:       build the print plugin (if you don't build it externally)
%bcond_without print
# gutenprint:  require gutenprint-plugin (instead of gimp-print-plugin) if
#              internal print plugin isn't built
%bcond_without gutenprint
# convenience: install convenience symlinks
%bcond_without convenience
# gudev:       use gudev to discover special input devices
%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 15 || 0%{?rhel} >= 7
# use gudev from F-15/RHEL7 on
%bcond_without gudev
%else
%bcond_with gudev
%endif
# aalib:       build with AAlib (ASCII art gfx library)
%if 0%{?rhel}
# don't use aalib on RHEL
%bcond_with aalib
%else
%bcond_without aalib
%endif
# hardening:   use various compiler/linker flags to harden binaries against
#              certain types of exploits
%bcond_without hardening
# Reset this once poppler picks up the updated xpdf version of "GPLv2 or GPLv3"
%bcond_with poppler


Summary:        GNU Image Manipulation Program
Name:           gimp
Epoch:          2
Version:        2.7.4
Release:        2%{?dist}.R

# Set this to 0 in stable, 1 in unstable releases
%global unstable 1

# Compute some version related macros
# Ugly hack, you need to get your quoting backslashes/percent signs straight
%global major %(ver=%version; echo ${ver%%%%.*})
%global minor %(ver=%version; ver=${ver#%major.}; echo ${ver%%%%.*})
%global micro %(ver=%version; ver=${ver#%major.%minor.}; echo ${ver%%%%.*})
%global binver %major.%minor
%global interface_age 0
%global gettext_version 20
%global lib_api_version 2.0
%if ! %unstable
%global lib_minor %(echo $[%minor * 100])
%global lib_micro %micro
%else # unstable
%global lib_minor %(echo $[%minor * 100 + %micro])
%global lib_micro 0
%endif # unstable

License:        GPLv3+
Group:          Applications/Multimedia
URL:            http://www.gimp.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%__id_u -n)
Obsoletes:      gimp-perl < 2:2.0
Obsoletes:      gimp < 2:2.6.0-3
BuildRequires:  chrpath >= 0.13-5
%if %{with aalib}
BuildRequires:  aalib-devel
%endif
BuildRequires:  alsa-lib-devel >= 1.0.0
BuildRequires:  babl-devel >= 0.1.6
BuildRequires:  cairo-devel >= 1.10.2
BuildRequires:  curl-devel >= 7.15.1
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  fontconfig-devel >= 2.2.0
BuildRequires:  freetype-devel >= 2.1.7
BuildRequires:  gdk-pixbuf2-devel >= 2.24.0
BuildRequires:  gegl-devel >= 0.1.8
BuildRequires:  glib2-devel >= 2.30.2
BuildRequires:  gnome-keyring-devel >= 0.4.5
BuildRequires:  gtk2-devel >= 2.24.7
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  jasper-devel
%if %{with lcms}
BuildRequires:  lcms-devel >= 1.16
%endif
BuildRequires:  libexif-devel >= 0.6.15
BuildRequires:  libgnomeui-devel >= 2.10.0
%if %{with gudev}
BuildRequires:  libgudev1-devel >= 167
%else
BuildRequires:  hal-devel >= 0.5.7
%endif
BuildRequires:  libjpeg-devel
BuildRequires:  libmng-devel
BuildRequires:  libpng-devel >= 1.2.37
BuildRequires:  librsvg2-devel >= 2.34.2
BuildRequires:  libtiff-devel
BuildRequires:  libwmf-devel >= 0.2.8
BuildRequires:  pango-devel >= 1.29.4
%if %{with poppler}
%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} > 8 || 0%{?rhel} > 5
BuildRequires:  poppler-glib-devel >= 0.12.4
%else
BuildRequires:  poppler-devel >= 0.12.4
%endif
%endif
BuildRequires:  python-devel
BuildRequires:  pygtk2-devel >= 2.10.4
BuildRequires:  pygobject2-devel
%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} > 10 || 0%{?rhel} > 5
BuildRequires:  webkitgtk-devel >= 1.6.1
%else
BuildRequires:  WebKit-gtk-devel >= 1.6.1
%endif
BuildRequires:  libX11-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXpm-devel
BuildRequires:  sed
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  findutils

Requires:       glib2 >= 2.28.8
Requires:       gtk2 >= 2.24.7
Requires:       pango >= 1.29.4
Requires:       freetype >= 2.1.7
Requires:       fontconfig >= 2.2.0
%if ! %{with print}
%if %{with gutenprint}
Requires:       gutenprint-plugin
%else
Requires:       gimp-print-plugin
%endif
%endif
Requires:       hicolor-icon-theme
Requires:       pygtk2 >= 2.10.4
Requires:       xdg-utils
Requires:       gimp-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Source0:        ftp://ftp.gimp.org/pub/gimp/v%{binver}/gimp-%{version}.tar.bz2

%description
GIMP (GNU Image Manipulation Program) is a powerful image composition and
editing program, which can be extremely useful for creating logos and other
graphics for webpages. GIMP has many of the tools and filters you would expect
to find in similar commercial offerings, and some interesting extras as well.
GIMP provides a large image manipulation toolbox, including channel operations
and layers, effects, sub-pixel imaging and anti-aliasing, and conversions, all
with multi-level undo.

%package libs
Summary:        GIMP libraries
Group:          System Environment/Libraries
License:        LGPLv3+

%description libs
The gimp-libs package contains shared libraries needed for the GNU Image
Manipulation Program (GIMP).

%package devel
Summary:        GIMP plugin and extension development kit
Group:          Development/Libraries
License:        LGPLv3+
Requires:       gimp-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gimp-devel-tools = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gtk2-devel
Requires:       glib2-devel
Requires:       pkgconfig

%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.

%package devel-tools
Summary:        GIMP plugin and extension development tools
Group:          Development/Tools
License:        LGPLv3+
Requires:       gimp-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel-tools
The gimp-devel-tools package contains gimptool, a helper program to build GNU
Image Manipulation Program (GIMP) plug-ins and extensions.

%package help-browser
Summary:        GIMP help browser plug-in
Group:          Applications/Multimedia
License:        GPLv3+
Obsoletes:      gimp < 2:2.6.0-3
Requires:       gimp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description help-browser
The gimp-help-browser package contains a lightweight help browser plugin for
viewing GIMP online help.

%prep
cat << EOF
--- 8< --- Build options ---------------------------------------------------
LCMS support:                 %{with lcms}
Python support:               %{with python}
MP support:                   %{with mp}
build static libs:            %{with static}
build internal print plugin:  %{with print}
include convenience symlinks: %{with convenience}
build the print plugin:       %{with print}
use gudev:                    %{with gudev}
%if ! %{with print}
prefer gutenprint over (external) gimp-print plugin:
                              %{with gutenprint}
%endif
build ASCII art plugin        %{with aalib}
harden binaries:              %{with hardening}
use poppler:                  %{with poppler}
--- >8 ---------------------------------------------------------------------
EOF

%setup -q -n gimp-%{version}

%build
%if %{with hardening}
# Use hardening compiler/linker flags because gimp is likely to deal with files
# coming from untrusted sources
%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global _hardened_build 1
%else
# fake things
export CFLAGS='-fPIC %optflags'
export CXXFLAGS='-fPIC %optflags'
export LDFLAGS='-pie'
%endif
%endif
%configure \
%if %{with python}
    --enable-python \
%else
    --disable-python \
%endif
%if %{with mp}
    --enable-mp \
%else
    --disable-mp \
%endif
%if %{with static}
    --enable-static \
%else
    --disable-static \
%endif
%if %{with print}
    --with-print \
%else
    --without-print \
%endif
%if %{with lcms}
    --with-lcms \
%else
    --without-lcms \
%endif
    --enable-gimp-console \
%if %{with aalib}
    --with-aa \
%else
    --without-aa \
%endif
%if %{with gudev}
    --with-gudev --without-hal \
%else
    --with-hal --without-gudev \
%endif
%ifos linux
    --with-linux-input \
%endif
%if use_poppler
    --with-poppler \
%else
    --without-poppler \
%endif
    --with-libtiff --with-libjpeg --with-libpng --with-libmng --with-libjasper \
    --with-libexif --with-librsvg --with-libxpm --with-gvfs --with-alsa \
    --with-webkit --with-dbus --with-script-fu --with-cairo-pdf

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

# makeinstall macro won't work here - libexec is overriden
make DESTDIR=%{buildroot} install

# remove rpaths
find %buildroot -type f -print0 | xargs -0 -L 20 chrpath --delete --keepgoing 2>/dev/null || :

%ifos linux
# remove .la files
find %buildroot -name \*.la -exec %__rm -f {} \;
%endif

#
# Plugins and modules change often (grab the executeable ones)
#
echo "%defattr (-, root, root)" > gimp-plugin-files
find %{buildroot}%{_libdir}/gimp/%{lib_api_version} -type f | sed "s@^%{buildroot}@@g" | grep -v '\.a$' >> gimp-plugin-files

# .pyc and .pyo files don't exist yet
grep "\.py$" gimp-plugin-files > gimp-plugin-files-py
for file in $(cat gimp-plugin-files-py); do
    for newfile in ${file}c ${file}o; do
        fgrep -q -x "$newfile" gimp-plugin-files || echo "$newfile"
    done
done >> gimp-plugin-files

%if %{with static}
echo "%defattr (-, root, root)" > gimp-static-files
find %{buildroot}%{_libdir}/gimp/%{lib_api_version} -type f | sed "s@^%{buildroot}@@g" | grep '\.a$' >> gimp-static-files
%endif

#
# Auto detect the lang files.
#
%find_lang gimp%{gettext_version}
%find_lang gimp%{gettext_version}-std-plug-ins
%find_lang gimp%{gettext_version}-script-fu
%find_lang gimp%{gettext_version}-libgimp
%find_lang gimp%{gettext_version}-tips
%find_lang gimp%{gettext_version}-python

cat gimp%{gettext_version}.lang gimp%{gettext_version}-std-plug-ins.lang gimp%{gettext_version}-script-fu.lang gimp%{gettext_version}-libgimp.lang gimp%{gettext_version}-tips.lang gimp%{gettext_version}-python.lang > gimp-all.lang

#
# Build the master filelists generated from the above mess.
#
cat gimp-plugin-files gimp-all.lang > gimp.files

%if %{with convenience}
# install convenience symlinks
ln -snf gimp-%{binver} %{buildroot}%{_bindir}/gimp
ln -snf gimp-%{binver}.1 %{buildroot}%{_mandir}/man1/gimp.1
ln -snf gimp-console-%{binver} %{buildroot}/%{_bindir}/gimp-console
ln -snf gimp-console-%{binver}.1 %{buildroot}/%{_mandir}/man1/gimp-console.1
ln -snf gimptool-%{lib_api_version} %{buildroot}%{_bindir}/gimptool
ln -snf gimptool-%{lib_api_version}.1 %{buildroot}%{_mandir}/man1/gimptool.1
ln -snf gimprc-%{binver}.5 %{buildroot}/%{_mandir}/man5/gimprc.5
%endif

%clean
rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f gimp.files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc docs/*.xcf*
%{_datadir}/applications/*.desktop

%dir %{_datadir}/gimp
%dir %{_datadir}/gimp/%{lib_api_version}
%{_datadir}/gimp/%{lib_api_version}/dynamics/
%{_datadir}/gimp/%{lib_api_version}/menus/
%{_datadir}/gimp/%{lib_api_version}/tags/
%{_datadir}/gimp/%{lib_api_version}/tips/
%{_datadir}/gimp/%{lib_api_version}/ui/
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{lib_api_version}
%dir %{_libdir}/gimp/%{lib_api_version}/environ
#%dir %{_libdir}/gimp/%{lib_api_version}/fonts
%dir %{_libdir}/gimp/%{lib_api_version}/interpreters
%dir %{_libdir}/gimp/%{lib_api_version}/modules
%dir %{_libdir}/gimp/%{lib_api_version}/plug-ins
%exclude %{_libdir}/gimp/%{lib_api_version}/plug-ins/help-browser
%dir %{_libdir}/gimp/%{lib_api_version}/python
#%dir %{_libdir}/gimp/%{lib_api_version}/tool-plug-ins

%{_datadir}/gimp/%{lib_api_version}/brushes/
%{_datadir}/gimp/%{lib_api_version}/fractalexplorer/
%{_datadir}/gimp/%{lib_api_version}/gfig/
%{_datadir}/gimp/%{lib_api_version}/gflare/
%{_datadir}/gimp/%{lib_api_version}/gimpressionist/
%{_datadir}/gimp/%{lib_api_version}/gradients/
# %{_datadir}/gimp/%{lib_api_version}/help/
%{_datadir}/gimp/%{lib_api_version}/images/
%{_datadir}/gimp/%{lib_api_version}/palettes/
%{_datadir}/gimp/%{lib_api_version}/patterns/
%{_datadir}/gimp/%{lib_api_version}/scripts/
%{_datadir}/gimp/%{lib_api_version}/themes/

%dir %{_sysconfdir}/gimp
%dir %{_sysconfdir}/gimp/%{lib_api_version}
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/controllerrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/gimprc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/gtkrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/unitrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/sessionrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/templaterc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/menurc

%{_bindir}/gimp-%{binver}
%{_bindir}/gimp-console-%{binver}

%if %{with convenience}
%{_bindir}/gimp
%{_bindir}/gimp-console
%endif

%{_mandir}/man1/gimp-%{binver}.1*
%{_mandir}/man1/gimp-console-%{binver}.1*
%{_mandir}/man5/gimprc-%{binver}.5*

%if %{with convenience}
%{_mandir}/man1/gimp.1*
%{_mandir}/man1/gimp-console.1*
%{_mandir}/man5/gimprc.5*
%endif

%{_datadir}/icons/hicolor/*/apps/gimp.png

%files libs
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libgimp-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimp-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpbase-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpbase-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpcolor-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpcolor-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpconfig-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpconfig-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpmath-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpmath-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpmodule-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpmodule-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpthumb-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpthumb-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpui-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpui-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpwidgets-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpwidgets-%{lib_api_version}.so.%{interface_age}

%if %{with static}
%files devel -f gimp-static-files
%else
%files devel
%endif
%defattr (-, root, root, 0755)
%doc HACKING README.i18n
%doc %{_datadir}/gtk-doc

%{_libdir}/*.so
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{lib_api_version}
%dir %{_libdir}/gimp/%{lib_api_version}/modules
%ifnos linux
%{_libdir}/*.la
%{_libdir}/gimp/%{lib_api_version}/modules/*.la
%endif
%{_datadir}/aclocal/*.m4
%{_includedir}/gimp-%{lib_api_version}
%{_libdir}/pkgconfig/*

%files devel-tools
%defattr (-, root, root, 0755)
%{_bindir}/gimptool-%{lib_api_version}
%{_mandir}/man1/gimptool-%{lib_api_version}.1*

%if %{with convenience}
%{_bindir}/gimptool
%{_mandir}/man1/gimptool.1*
%endif

%files help-browser
%defattr (-, root, root, 0755)
%{_libdir}/gimp/%{lib_api_version}/plug-ins/help-browser

%changelog
* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 2:2.7.4-2
- rebuild for gcc 4.7

* Thu Dec 15 2011 Nils Philippsen <nils@redhat.com> - 2:2.7.4-1
- version 2.7.4 (unstable, see http://developer.gimp.org/NEWS for details)
- update dependency versions
- don't suppress abrt reporting, don't redirect bug reports to upstream

* Tue Aug 30 2011 Nils Philippsen <nils@redhat.com> - 2:2.7.3-1
- version 2.7.3 (unstable, see http://developer.gimp.org/NEWS for details)
  - change license to GPLv3+/LGPLv3+
  - update required versions of dependencies
  - build with cairo-pdf, jasper, require jasper-devel for building
  - build without poppler as that currently is GPLv2 only, thus incompatible
    with LGPLv3 gimp libraries (use postscript plugin for PDF import
    meanwhile), future poppler versions will be "GPLv2 or GPLv3", i.e.
    compatible again
  - clean up configure options, compiler/linker flags
  - suppress abrt bug reporting for unstable releases
  - remove all patches (obsolete, woo!)
  - add new files, remove files that are not installed any longer
- use %%global instead of %%define
- replace hal, minorver, microver, interfacever, gimp_lang_ver macros with
  gudev, lib_minor, lib_micro, lib_api_version, gettext_version macros
- compute more version macros (ugly, but convenient)
- use gudev from Fedora 15 on
- use convenience macro for hardening binaries from F-16 on

* Fri Aug 12 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-21
- actually apply startup-warning patch
- fix heap corruption and buffer overflow in file-gif-load plugin
  (CVE-2011-2896)

* Thu Aug 04 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-20
- fix goption warning on startup, patch by Mikael Magnusson

* Wed Aug 03 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-19
- remove obsolete gtkhtml2-devel build requirement

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 2:2.6.11-18
- Rebuild (poppler-0.17.0)

* Fri Jun 24 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-17
- rebuild against new cfitsio

* Fri Jun 10 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-16
- guard against crash due to quitting while DND is processed (#711952)

* Tue Jun 07 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-15
- drop support for building with non-modular X
- ensure file-xpm plugin is built (#710207)

* Mon May 23 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-14
- fix buffer overflows in sphere-designer (CVE-2010-4541),
  gfig (CVE-2010-4542), lighting (CVE-2010-4540) plugins

* Mon May 23 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-13
- harden PSP plugin against bogus input data (CVE-2010-4543, CVE-2011-1782)

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 2:2.6.11-12
- Update desktop database, icon cache scriptlets

* Fri May 06 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-11
- simplify poppler-0.17 patch to avoid adding to libgimp (#698157)

* Wed May 04 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-10
- don't use poppler/gdk_pixbuf API removed in poppler >= 0.17 (#698157)
- remove obsolete configure options

* Tue Mar 15 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-9
- don't use HAL from F-16/RHEL-7 on
- explicitly use GIO/GVFS rather than gnome-vfs

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2:2.6.11-8
- Rebuild (poppler-0.16.3)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.6.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Nils Philippsen <nils@redhat.com> - 2:2.6.11-6
- avoid traceback in pyslice plugin (#667958)

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 2:2.6.11-5
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2:2.6.11-4
- rebuild (poppler)

* Tue Nov 09 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.11-3
- avoid traceback in colorxhtml plugin (#651002)

* Sat Nov 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 2:2.6.11-2
- rebuilt (poppler)

* Mon Oct 04 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.11-1
- version 2.6.11

  Overview of Changes from GIMP 2.6.10 to GIMP 2.6.11
  ===================================================

  * Bugs fixed:

   631199 - Printing and Print preview broken with cairo 1.10
   572865 - Parasite handling had problems and can cause crashing
   628893 - Error with string-append and gimp-drawable-get-name
   623850 - (Paco) Recursive Gaussian Filter error
   624487 - Fix incorrect "wrap mode" documentation values in Edge plug-in
   557380 - Difference of Gaussians gives blank doc if "Invert" selected
   627009 - Image type filter doesn't include .rgba SGI files
   626020 - Console window opening on file-ps-load
   624698 - Wood 1 and Wood 2 have bad alpha value
   624275 - Image saved from google docs generates a
            'gimp-image-set-resolution' error message

  * Updated translations:

   German (de)
   Spanish (es)
   Italian (it)
   Japanese (ja)
   Romanian (ro)
   Chinese (Hong Kong) (zh_HK)
   Chinese (Taiwan) (zh_HK)

* Tue Aug 24 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.10-5
- don't require gtk-doc but own %%{_datadir}/gtk-doc (#604355, #604169)

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 2:2.6.10-4
- rebuild (poppler)

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2:2.6.10-3
- recompiling .py files against Python 2.7 (rhbz#623309)

* Mon Jul 09 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.10-2
- distribute license and other documentation with gimp-libs

* Fri Jul 09 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.10-1
- version 2.6.10

  Overview of Changes from GIMP 2.6.9 to GIMP 2.6.10
  ==================================================

  * Bugs fixed:

   613328 - TGA files saved with incorrect header yOrigin data
   623290 - Save As... does not save Windows Bitmap as default in dialog
   621363 - CMYK decompose broken
   595170 - brush - color from gradient works wrong in greyscale
   613838 - Error in gimp-hue-saturation PDB call
   622608 - GIMP crashes when clicking any scroll bar from combo boxes
   565459 - newly opened images are put into the background

  * Updated translations:

   German (de)
   Italian (it)
   Romanian (ro)
   Portuguese (pt)

- remove obsolete combo-popup patch
- update script-fu-ipv6 patch

* Mon Jul 05 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.9-5
- rebuild against libwebkitgtk (instead of libwebkit)

* Tue Jun 29 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.9-4
- script-fu: make rest of server IPv6-aware (#198367)

* Mon Jun 28 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.9-3
- script-fu: make logging IPv6-aware (#198367)

* Fri Jun 25 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.9-2
- fix clicking scroll bar buttons from combo boxes

* Wed Jun 23 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.9-1
- version 2.6.9

  Overview of Changes from GIMP 2.6.8 to GIMP 2.6.9
  =================================================

  * Bugs fixed:

   612618 - Font selection remains visible
   622234 - gimp.desktop: image/x-psd in MimeTypes twice
   622196 - Unportable test(1) construct in configure script
   620604 - Description of "histogram" procedure is slightly inaccurate
   541586 - Tool options not saved/loaded correctly?
   614153 - Importing PDF files with long titles
   600112 - blur-gauss-selective.exe crashes
   599233 - Dialog of "Save as BMP" ignores changes which are not made
            with a mous
   565001 - Text-Tool crashes when edit a 2.4.2 version xcf
   610478 - Layer preview suddenly stops getting updated
   609026 - leaks shared memory
   609056 - Exporting to Alias PIX format fails
   608188 - a few strings in Save as... > Raw image data dialog are always
            in English
   604820 - GEGL Operation "path" crashes GIMP
   603711 - Crashes when using path tool
   607242 - GIMP 2.7.0 fails to build against libpng 1.4.0
   606372 - Saving to .ppm fails on indexed colorspace
   605237 - the "Antialiasing..." message in the progress bar does not show
            translated
   604508 - gimp-layer-new-from-visible should work from updated projection

  * Updated and new translations:

   Asturian (ast)
   Basque (eu)
   Burmese (my)
   Catalan (ca)
   Chinese (Hong Kong) (zh_HK)
   Chinese (Taiwan) (zh_HK)
   German (de)
   Italian (it)
   Latvian (lv)
   Low German (nds)
   Romanian (ro)
   Simplified Chinese (zh_CN)
   Slovenian (sl)
   Ukrainian (uk)
   Valencian (ca@valencia)

- remove obsolete gtk219, never-stack-trace-desktop, indexed-pnm patches
- don't manually provide "gimp-libs%%{?_isa}" in gimp-libs
- don't package %%{_datadir}/gtk-doc/html, but dirs beneath

* Wed Jun 23 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-10
- get rid of obsolete gimp-plugin-mgr

* Tue Jun 22 2010 Matthias Clasen <mclasen@redhat.com> - 2:2.6.8-9
- Rebuild against new poppler

* Fri Jun 18 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-8
- backport fix for saving indexed PNM files (#605615)

* Mon Apr 19 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-7
- add --stack-trace-mode=never to desktop file

* Wed Mar 24 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-6
- backport: statusbar code needed for GTK+ >= 2.19.1 (#559726)

* Fri Feb 26 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-5
- require gtk-doc in devel package

* Thu Feb 25 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-4
- add missing explicit libraries

* Wed Feb 24 2010 Nils Philippsen <nils@redhat.com>
- backport: fix building with "gold" linker
- add more explicit libraries

* Wed Jan 27 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-3
- remove wrong dependency (#558836)

* Mon Jan 25 2010 Nils Philippsen <nils@redhat.com> - 2:2.6.8-2
- rebuild against new babl

* Wed Jan 20 2010 Nils Philippsen <nils@redhat.com>
- use %%_isa instead of %%_arch for architecture-specific dependencies

* Fri Dec 11 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.8-1
- version 2.6.8

  Overview of Changes from GIMP 2.6.7 to GIMP 2.6.8
  =================================================

  * Bugs fixed:

   470698 - MapObject cannot modify highlight
   593848 - FG color changed to black when FG-BG Editor tab created
   594651 - layer.scale() raises RuntimeError
   594998 - Keyboard shortcuts does not work for first image when dock
            is focused
   599765 - F1 key on gimp-tool-align in menu have wrong link and it
            open gimp-tool-move
   600484 - Gimp BMP Integer Overflow Vulnerability
   600741 - "read_channel_data()" Integer Overflow Vulnerability
   601891 - gimp_image_get_selection returns None
   602761 - plug-in-grid: Parameters Horizontal/Vertical Spacing and
            Horizontal/Vertical Offset are reversed.
   603995 - PCX plugin doesn't sanitize input to avoid allocation overflows.
   603998 - PCX: Calculating amount of memory to allocate may overflow.
   604000 - SGI: sanitize input
   604001 - SGI: Calculating amount of memory to allocate may overflow.
   604002 - SGI: RLE encoded input data may write beyond allocated buffers
   604004 - SGI: allocate memory consistently
   604008 - GBR, PAT: sanitize input data
   604078 - Crash when pressing Backspace with Free Select Tool

  * Updated and new translations:

   Basque (eu)
   British English (en_GB)
   Czech (cs)
   French (fr)
   Greek (el)
   Italian (it)
   Japanese (ja)
   Norwegian Nynorsk (nn)
   Polish (pl)
   Romanian (ro)
   Russian (ru)
   Simplified Chinese (zh_CN)

- remove obsolete bmp-hardening, psd-hardening patches

* Tue Nov 17 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.7-3
- avoid overflow in the BMP image file plugin (#537356)
- avoid overflow in the PSD image file plugin (#537370)
- update jpeg-units patch

* Tue Aug 18 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.7-2
- BR: webkitgtk-devel/WebKit-gtk-devel >= 1.1.0

* Fri Aug 14 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.7-1
- version 2.6.7

  Overview of Changes from GIMP 2.6.6 to GIMP 2.6.7
  =================================================

  * Bugs fixed:

   591017 - Tablet pan is not working as fast as it should
   577581 - Crashes when using any colors tool/function on Windows
   589667 - GIMP crashes when clicking GEGL Operation on Windows
   569833 - file-jpeg-save erroneous with small quality values
   590638 - Changing palettes from list to grid view loses "locked to dock"
            status
   589674 - "Send by Email" does not update "Filename"
   589674 - "Send by Email" does not update "Filename"
   586851 - Transparent BMP files fail to load
   589205 - help-browser uses deprecated (and sometimes broken) webkit call
   582821 - 'Sphere Designer' does not reset correctly...
   570353 - first time open of .svg file ignores the requested units
   555777 - Export to MNG animation fails
   577301 - Dithering with transparency is broken for "positioned" method
   493778 - metadata plug-in crashes on some images
   567466 - PNG comment not found if more than 1 tEXt chunks
   585665 - Exporting to PSD with a blank text layer creates a corrupt file
   586316 - Levels tool does not adjust output levels correctly if input
            levels are changed
   569661 - Import from PDF throws errors when entering resolution in
            pixels per millimetre
   567262 - Black pixels appear in "Spread" filter preview
   554658 - Path Dialog: Path preview pics not to see constantly
   167604 - gimp_gradient_get_color_at() may return out-of-bounds values
   567393 - Rectangle select tool size shrinks to 0 if size is larger than
            the image and the up or down arrow is pressed
   587543 - crash when invoking certain actions by keyboard shortcut
   563029 - Closing maximized image doesn't restore document window size
   585488 - Perspective transformation on a layer with a mask causes crash
   586008 - GIMP crashes when right-click canceling a drawing action initiated
            outside layer boundaries
   584345 - when printing, the number of copies should be reset to 1
   557061 - Alpha to Logo
   472644 - Rotate with clipping crops the whole layer
   577575 - transform tool fills underlying extracted area wrongly
   555738 - Image display is wrong after undoing canvas size
   577024 - help-browser plugin crashes when used with webkit 1.1.3
   555025 - Action GEGL box widgets weirdness

  * Updated and new translations:

   Czech (cs)
   Danish (da)
   German (de)
   Spanish (es)
   Basque (eu)
   Finnish (fi)
   Hungarian (hu)
   Italian (it)
   Gujarati (gu)
   Japanese (ja)
   Kannada (kn)
   Marathi (mr)
   Norwegian bokmål (nb)
   Oriya (or)
   Portuguese (pt)
   Romanian (ro)
   Sinhala (si)
   Swedish (sv)
   Simplified Chinese (zh_CN)
   Traditional Chinese - Hong Kong (zh_HK)
   Traditional Chinese - Taiwan (zh_TW)

- remove obsolete gegl-babl-versions-check, help-browser-webkit patches
- comment/explain patches

* Fri Jul 24 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-8
- rebuild with chrpath >= 0.13-5 (#513419)

* Thu Jul 16 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-7
- rebuild against gegl-0.1 (#510209)

* Mon Jun 29 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-6
- really fix help browser crash with new WebKit versions (#508301)

* Sat Jun 27 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-5
- fix help browser crash with new WebKit versions (#508301)
- BR: webkitgtk-devel from F-11 on

* Fri Jun 05 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-4
- don't build against aalib on RHEL
- use backported patch to correctly check gegl/babl versions

* Tue Apr 14 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-3
- remove rpaths from binaries (#495670)

* Mon Mar 30 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-2
- minimize dialogs with single image window (#492796, backported from trunk,
  original patch by Sven Neumann)

* Wed Mar 18 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.6-1
- version 2.6.6

  Overview of Changes from GIMP 2.6.5 to GIMP 2.6.6
  =================================================

  * Bugs fixed:

   571117 - lcms plug-in crashes on broken profile
   575154 - changing the help browser preference may not work
   573542 - blur plugin: bug in the first line
   572403 - gimp-2.6 crashed with SIGSEGV in IA__g_object_get()
   573695 - 1-bit white background saved as PBM becomes all black
   573488 - Small bug in Filter>Distorts>Ripple
   572156 - top left pixel position/coordinate is not 0,0 but 1,1
   472644 - Rotate with clipping crops the whole layer

  * Updated translations:

   German (de)
   Spanish (es)
   Estonian (et)
   Basque (eu)
   French (fr)
   Italian (it)
   Portuguese (pt)
   Simplified Chinese (zh_CN)

* Tue Mar 17 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.5-5
- require pygtk2 >= 2.10.4 (#490553)

* Tue Mar 10 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.5-4
- use correct fix from upstream to avoid crashes (#486122)
- use -fno-strict-aliasing, PIC/PIE compilation flags

* Mon Mar 09 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.5-3
- rebuild against new WebKit
- define deprecated gtk functions to avoid crashes (#486122)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.5-1
- version 2.6.5

  Overview of Changes from GIMP 2.6.4 to GIMP 2.6.5
  =================================================

  * Bugs fixed:

   571628 - Scaling image to 25% turn background from white to grey
   567840 - GIMP's GtkScaleButton conflicts with GTK's
   569043 - GEGL tool - missing Operation Settings for all sub-tools
   568890 - don't rely on GtkAction implementation details
   568909 - wrong RGB values for color names in libgimpcolor/gimprgb-parse.c
   568839 - wrong hex RGB value for the color names slategrey and slategray
   559408 - Brushes dragged to the image window look strange
   563337 - Rectangle Select Tool does not allow 1:1 fixed ratio
   568016 - Black pullout parameter of plug-in-newsprint has no effect
   562818 - First image opened in GIMP offset
   562213 - Align Tool doesn't work properly if it is the active tool
            at startup

  * Updated translations:

   Spanish (es)
   Estonian (et)
   Hindi (hi)
   Italian (it)
   Brazilian Portuguese (pt_BR)
   Romanian (ro)
   Russian (ru)
   Serbian (sr)
   Tamil (ta)
   Simplified Chinese (zh_CN)

* Wed Jan 07 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.4-3
- split off gimptool into new gimp-devel-tools subpackage to avoid multilib
  conflicts (#477789)
- require poppler-glib-devel for building from F9 on (#478691)
- fix gimp-devel package group

* Sun Jan 04 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.4-2
- enable building with aalib

* Thu Jan 01 2009 Nils Philippsen <nils@redhat.com> - 2:2.6.4-1
- version 2.6.4

  Overview of Changes from GIMP 2.6.3 to GIMP 2.6.4
  =================================================
  
  * Bugs fixed:
  
   565223 - Perspective transformation jagged edges / comb effect
   563985 - jpg save dialog: "cancel" is treated like "commit"
            for settings
   564087 - Using clone tool on a layer with a part out of canvas
            causes crashes
   564593 - crash when the drawable is changed while a color tool
            is active
   564869 - GIMP crashes on selecting Tools->GEGL operation
   565138 - python-fu-foggify does not check if image is in rgb mode
   563130 - Hue selection mode does not cross the 0-360 degrees line
   563179 - Scrollbars not resized when we extend the canvas size
   562459 - PF_PALETTE: 'TypeError' when used in a plugin that is
            registered in <Image>
   562427 - Compilation with --as-needed
   562386 - PF_SLIDER and PF_SPINNER 'Step' values do not change
            consistently...
   562366 - Default image dimensions are not correctly
            transferred in the file/new dialog box
   561899 - GIMP can't save to mounted filesystem if file exists
  
  * Updated translations:
  
   Greek (el)
   Hindi (hi)
   Hungarian (hu)
   Italian (it)
   Japanese (ja)
   Korean (ko)
   Slovenian (sl)
   Swedish (sv)
   Tamil (ta)
   Simplified Chinese (zh_CN)
- add BuildRequires: aalib-devel

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2:2.6.3-3
- Rebuild for Python 2.6

* Mon Nov 24 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.3-2
- own /usr/lib/gimp/2.0/interpreters (#473594)

* Mon Nov 24 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.3-1
- version 2.6.3

  Overview of Changes from GIMP 2.6.2 to GIMP 2.6.3
  =================================================

  * Bugs fixed:

   558454 - Plugin Map Color Range disappears from GIMP
   559239 - Error while loading psd-data
   560903 - Explicit zooming with e.g. '1' should handle
            zoom-focus better
   560245 - Zoom selection always centered in the Navigation tab
   559490 - Wrong lang tags for 'no'
   559292 - SOTA Chrome cannot accept different textures
   560375 - Clearing an already empty document history crashes GIMP
   559580 - Image windows need better default locations
   560283 - "Scale image..." causes distortion around edges
   559716 - Changing crop size in Crop Tool Options can make UI
            unresponsive
   558549 - Stroking a single-point path with a paint tool
            crashes GIMP
   559015 - Move tool gives bad information about px moved
   558660 - help behavior for locales without manual translation

  * Updated translations:

   Belarusian (be)
   Dutch (nl)
   German (de)
   Japanese (ja)
   Lithuanian (lt)
   Norwegian Bokmål (nb)
   Norwegian Nynorsk (nn)
   Polish (pl)
   Romanian (ro)

* Fri Nov 14 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.2-3
- bump release

* Tue Nov 11 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.2-2
- backport: use size units in JPEG save preview (#469551)

* Fri Oct 31 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.2-1
- version 2.6.2

  Overview of Changes from GIMP 2.6.1 to GIMP 2.6.2
  =================================================

  * Bugs fixed:

   557950 - Scaling in Gimp 2.6 is much slower than in Gimp 2.4
   558215 - unit and zoom entries in Statusbar not visible
   558451 - Cannot build GIMP using Sun CC on Solaris 2.8
   558420 - projection incorrect with alpha-less layers
   556603 - Zoom region always zooms in center of image
   557870 - "Qmask" message popping up here and there
   557705 - compatibility with GEGL > 0.0.20
   556248 - Scaling gives 'jagged' edges
   556804 - Zoom drop down doesn't update
   524615 - Print not to scale
   555246 - gimp crashes when a file is opened while a preview is generating
   556741 - Alpha layer automatically added (in psd format)
   556182 - Could you please explain a few strings [I18N]
   555697 - build fails if configured with --without-libjpeg
   134956 - Curves tool doesn't save free curves

  * Updated translations:

   Czech (cs)
   Danish (da)
   Finnish (fi)
   French (fr)
   Japanese (ja)
   Polish (pl)
   Brazilian Portuguese (pt_BR)
   Swedish (sv)
   Simplified Chinese (zh_CN)
- update xdg-open patch

* Tue Oct 28 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.1-2
- update required versions of some packages (#467065)

* Fri Oct 10 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.1-1
- version 2.6.1

  Overview of Changes from GIMP 2.6.0 to GIMP 2.6.1
  =================================================

  * Bugs fixed:

   555587 - PSD file crashes PSD plug-in
   555222 - PSD Load Plugin: unsupported compression mode
   555362 - gimp-remote is not working properly
   555280 - some gif files will not be open
   554890 - JPEG Save Options Dialog does not remember
   554966 - Gimp crashes creating a new image using a template
   554785 - Compile failure on uri-backend-libcurl
   554646 - Opening Help crashes GIMP with lqr-plugin installed
   553534 - centering issues after image scaling and setting zoom
   554898 - Compile failure on uri-backend-wget.c

  * Updated translations:

   Belarusian (be)
   Catalan (ca)
   Finnish (fi)
   French (fr)
   Japanese (ja)
   Macedonian (mk)
   Punjab (pa)
   Brazilian Portuguese (pt_BR)
   Romanian (ro)
   Slovenian (sl)
   Swedish (sv)

* Wed Oct 08 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.0-3
- split off help browser plugin
- let gimp and gimp-help-browser obsolete older gimp versions to allow seamless
  upgrades

* Tue Oct 07 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.0-2
- move gimptool to devel subpackage
- make gimp-plugin-mgr not require gimptool/pkg-config (#465869)

* Thu Oct 02 2008 Nils Philippsen <nils@redhat.com> - 2:2.6.0-1
- version 2.6.0
- remove obsolete htmlview patch
- remove obsolete distro version dependent defaults
- don't use custom CFLAGS

* Mon Sep 22 2008 Nils Philippsen <nils@redhat.com> - 2:2.4.7-4
- don't require desktop-file-utils (#463049, patch by Ville Skyttä)

* Wed Sep 17 2008 Nils Philippsen <nils@redhat.com> - 2:2.4.7-3
- don't make pyconsole.py plug-in executable as upstream indicates it shouldn't
  be

* Wed Sep 17 2008 Nils Philippsen <nils@redhat.com> - 2:2.4.7-2
- Merge review:
  - convert spec file to UTF-8
  - remove unneeded gimp2, gimp-beta obsoletes
  - quote macros in changelog
  - use only spaces, not tabs
  - make pyconsole.py plug-in executable (upstream bug #552601)

* Fri Aug 22 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.7-1
- version 2.4.7

  Changes in GIMP 2.4.7
  =====================

  - fixed issue in GIF load plug-in (bug #535888)
  - fixed event handling in MIDI controller (bug #537960)
  - fixed handling of the 'Highlight' tool option in Crop and Rectangle
    Select tools (bug #536582)
  - various fixes to the Python bindings:
    - fixed crash with Python 2.5 on 64 bit systems (bug #540629)
    - added missing validity checks (bug #536403)
    - allow to pass None for PDB_DISPLAY
  - plugged a memory leak in gimp-text-get-extents-fontname PDB call
  - fixed potential timeout issues in org.gimp.GIMP.UI D-Bus service
  - fixed endianness issue in the ICO save plug-in (bug #529629)
  - translation fixes and updates (be, it, lt, nn, vi)

* Fri May 30 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.6-1
- version 2.4.6

  Changes in GIMP 2.4.6
  =====================

  - fixed handling of the "antialias" tool option (bug #521069)
  - when loading a TIFF image, always set a filename on it (bug #521436)
  - fixed initial state of curve type in Curves tool (bug #523873)
  - fixed potential crash in the Dicom load plug-in
  - respect the brush mask in the Heal tool (bug #521433)
  - plugged some minor memory leaks
  - fixed a glitch in the DND code (bug #317992)
  - gimp-image-convert() must not accept palettes with > 256 colors (bug
    #525471)
  - fixed parameter description in the Map Object plug-in (bug #526679)
  - fixed compilation of unit tests on Mac OS X (bug #528160)
  - fixed handling of "argc-lower-val-y" PDB parameter in Curve Bend plug-in
  - fixed overlap problem in Hue-Saturation tool (bug #527085)
  - fixed asymmetry in Unsharp Mask plug-in (bug #530077)
  - don't show non-existant color profiles in the selector (bug #528958)
  - fixed issues with default aspect ratio in the Crop tool (bug #532057)
  - fixed compilation of the PDF import plug-in with libpoppler 0.8
  - fixed bug in clipboard brush code (bug #532886)
  - corrected layer mask flag in PSD save plug-in (bug #526811)
  - fixed an issue with tablets and newer X.Org releases
  - keep the JPEG save plug-in from writing an empty EXIF tag (bug #529469)
  - fixed crash in Selective Gaussion Blur plug-in (bug #529280)
  - added new translations (Belarusian, Catalan, Norwegian Nynorsk)
  - translation fixes and updates
    (ar, ca, de, el, es, fi, fr, hu, it, ko, pl, pt_BR, ro, sv)

* Mon Mar 03 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.5-1
- version 2.4.5

  Changes in GIMP 2.4.5
  =====================

  - fixed a regression introduced by the brush cursor optimization
    (bug #514309)
  - fixed bug in transform tool preview (bug #340965)
  - fixed PSD export of images with layer masks
  - fixed base64 encoding routine of the Mail plug-in
  - use the correct background color when creating a new image
    (bug #514082)
  - explicitly link libgimpthumb with GLib (bug #515566)
  - improved selection of the font sample string (bug #514021)
  - unified handling of "Enter" and "Space" keysyms (bug #516544)
  - fixed bug in the Glossy script when used with a pattern (bug #517285)
  - correctly record dimensions in Exif data when saving as JPEG
    (bug #517077)
  - fixed sensitivity of plug-in menu items (bug #517683)
  - fixed potential crashes in Wind, Warp, Small Tiles and Apply Canvas
    plug-ins (bug #516369)
  - added default keyboard shortcut for "Paste As New Image"
    (Ctrl-Shift-V)
  - added default keyboard shortcut for "Copy Visible" (Ctrl-Shift-C)
  - fixed missing preview update in Curves tool (bug #518012)
  - fixed a bug in the Frosty Logo script (bug #472316)
  - fixed backward transformations using the PDB (bug #518910)
  - translation fixes and updates (de, eu, eo, fr, he, hu, it, ja, ko)

* Mon Feb 18 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.4-2
- let gimp-libs provide, gimp and gimp-devel require "gimp-libs-%%{_arch}"
  (#433195)

* Wed Jan 30 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.4-1
- version 2.4.4

  Changes in GIMP 2.4.4
  =====================

  - fixed typo in stock icon name
  - fixed handling of PSD files with empty layer names (bug #504149)
  - merged TinyScheme bug-fixes
  - removed duplicate entry from Tango palette
  - corrected parameter range in Chip Away script (bug #506110)
  - reduced redraw priority and speed of the marching ants (bug #479875)
  - fixed out-of-bounds array access in Convolution Matrix plug-in
  - reduced rounding errors in Convolution Matrix plug-in (bug #508114)
  - fixed potential crash on missing CMYK color profile
  - fixed crash in Bumpmap plug-in when called from some scripts (bug #509608)
  - Equalize should not equalise the alpha channel (bug #510210)
  - increased the number of points the ImageMap plug-in can handle (bug #511072)
  - adjusted the priority of the projection renderer (bug #511214)
  - smooth the brush mask to get a simpler cursor boundary (bug #304798)
  - show the selection even if the image window is invisible (bug #505758)
  - allow to commit a pending rectangular selection using Enter (bug #511599)
  - fixed bug in image dirty state logic (bug #509822)
  - improved GIMPressionist preformance and reduced startup time (bug #512126)
  - fixed a crash in the Convert to Color Profile plug-in (bug #512529)
  - merged some other minor fixes from trunk
  - translation updates (de, it, lt, ru, sv, uk)

* Mon Jan 28 2008 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.3-2
- don't package static libraries (#430330)
- use %%bcond_... macros for package options

* Mon Dec 17 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.3-1
- version 2.4.3

  Changes in GIMP 2.4.3
  =====================

  - avoid filename encoding problems in the WMF import plug-in (bug #499329)
  - fixed horizontal flipping of linked layers (bug #499161)
  - fixed a missing update in the Lighting plug-in UI (bug #500317)
  - fixed a potential crash in the projection code (bug #500178)
  - fixed a minor Makefile issue (bug #500826)
  - removed some pointless warnings from the JPEG and TIFF load plug-ins
  - fixed size calculation for the image size warning dialog (bug #329468)
  - fixed loading of tool options for the rectangle tools (bug #498948)
  - push/pop a context in the Fog filter
  - fixed potential crashes in the Python binding
  - corrected grid drawing with non-integer spacing (bug #502374)
  - fixed grid snapping for coordinates less than the grid offset
  - made the healing brush work properly when dragged (bug #492575)
  - update tool state when a device change happens (bug #493176)
  - improved validation of strings sent over the wire (bug #498207)
  - fixed integer check in Script-Fu (bug #498207)
  - fixed potential out-of-memory problem in Script-Fu
  - translation updates (ca, cs, de, gl, it, ko, lt, sv, uk)

* Wed Nov 28 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.2-2
- fix typo to build internal print plugin from F8 onwards (#401931)

* Thu Nov 22 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.2-1
- version 2.4.2

  Changes in GIMP 2.4.2
  =====================

  - removed broken and useless HSV Graph script (bug #491311)
  - update the histogram when a color correction tool is cancelled (bug #493639)
  - fixed a crash with certain plug-in or script descriptions (bug #492718)
  - corrected a tooltip (bug #495564)
  - fixed a crash when GIMP is run without any modules (bug #495863)
  - fixed error handling in the TIFF plug-in
  - fixed a problem with Sample points
  - fixed a crash when merging layers in indexed image (bug #495990)
  - update the histogram when painting (bug #494049)
  - fixed another problem with merge operations on indexed images (bug #496437)
  - fixed crash in TIFF plug-in when saving indexed images (bug #497103)
  - changed defaults so that a system monitor profile is only used when the
    user explicitely enabled this feature (bug #496890)
  - fixed endless loop when running equalize on transparent areas (bug #497291)
  - fixed heap corruption in GimpColorScale widget that caused a crash in the
    Compose plug-in (bug #399484)
  - fixed use of background color in Particle Trace script (bug #498282)
  - set the image menu insensitive when there's no image opened (bug #498511)
  - translation updates (ca, et, it, lt, pt, pt_BR, sr, sv)

* Wed Oct 31 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.1-1
- version 2.4.1

  Changes in GIMP 2.4.1
  =====================

  - fixed a minor display rendering problem
  - improved the workaround for broken graphics card drivers (bug #421466)
  - fixed a crash with broken scripts and plug-ins (bug #490055)
  - fixed potential syntax error in configure script (bug #490068)
  - fixed parsing of floating point numbers in Script-Fu (bug #490198)
  - fixed potential crash when converting an indexed image to RGB (bug #490048)
  - update the histogram while doing color corrections (bug #490182)
  - fixed another crash with broken plug-ins (bug #490617).
  - translation updates

* Mon Oct 29 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-4
- use either htmlview or xdg-open in documentation instead of firefox (#355801)

* Thu Oct 25 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-3
- add epoch to obsoletes

* Wed Oct 24 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-1
- version 2.4.0
- use xdg-open instead of htmlview on Fedora 7 and later
- change hicolor-icon-theme requirement to be "uncolored" (without
  "(post)"/"(postun)")
- don't let gtk-update-icon-cache fail scriptlets

* Fri Sep 07 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-0.rc3.2
- build internal print plugin, don't require external print plugins on Fedora 8
  and later

* Fri Sep 07 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-0.rc3.1
- version 2.4.0-rc3

* Fri Sep 07 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-0.rc2.2
- rebuild to pick up new version of poppler

* Tue Sep 04 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-0.rc2.1
- version 2.4.0-rc2

* Thu Aug 16 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.4.0-0.rc1.1
- version 2.4.0-rc1
- change license tags to GPLv2+ (main app), LGPLv2+ (libs and devel)
- drop libXt-devel build requirement
- build-require pygobject2-devel directly
- don't let %%postun fail
- remove obsolete buildroot, gimphelpmissing, icontheme, gifload, gimptool
  patches
- update htmlview patch
- use more distinct build root
- use %%buildroot consistently
- explicitely enable configure options
- more versionized build requirements
- don't rebuild autofoo files
- reformat spec file a bit

* Fri Jul 13 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.17-1
- version 2.2.17

  Bugs fixed in GIMP 2.2.17
  =========================

  - fixed regression in PSD load plug-in (bug #456042)
  - fixed crash when loading a corrupt PSD file (bug #327444)
  - work around for Pango appending " Not-Rotated" to font names 

* Wed Jul 11 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.16-2
- don't let gimp-plugin-mgr --uninstall fail %%post scriptlet

* Mon Jul 09 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.16-1
- version 2.2.16

  Bugs fixed in GIMP 2.2.16
  =========================

  - improved input value validation in several file plug-ins (bug #453973)
  - improved handling of corrupt or invalid XCF files
  - guard against integer overflows in several file plug-ins (bug #451379)
  - fixed handling of background alpha channel in XCF files (bug #443097)
  - improved forward compatibility of the config parser
  - fixed crash when previewing some animated brushes (bug #446005)

- remove obsolete psd-invalid-dimensions patch

* Wed Jun 27 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.15-3
- refuse to open PSD files with insanely large dimensions (#244400, fix by Sven
  Neumann)

* Wed Jun 13 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.15-2
- require gutenprint-plugin or gimp-print-plugin (#243593)

* Thu May 31 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.15-1
- version 2.2.15

  Bugs fixed in GIMP 2.2.15
  =========================
  
  - fixed parsing of GFig files with CRLF line endings (bug #346988)
  - guard against a possible stack overflow in the Sunras loader (bug #433902)
  - fixed definition of datarootdir in gimptool-2.0 (bug #436386)
  - fixed Perspective tool crash on Mac OS X (bug #349483)
  - fixed area resizing in the Image Map plug-in (bug #439222)
  - added missing library in gimptool-2.0 --libs output
  - added new localizations: Occitan and Persian

- remove obsolete sunras-overflow patch

* Tue May 01 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.14-5
- don't let gimp-plugin-mgr --uninstall fail %%pre/%%preun scriptlets (#238337)

* Mon Apr 30 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.14-4
- fix plugin symlinks handling better (#238337)

* Mon Apr 30 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.14-3
- don't erroneously delete symlinks to external plugins when updating (#238337)

* Mon Apr 30 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.14-2
- avoid buffer overflow in sunras plugin (#238422)

* Tue Apr 24 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.14-1
- version 2.2.14
  
  Bugs fixed in GIMP 2.2.14
  =========================
  
  - avoid crashing on newer versions of the winicon format (bug #352899)
  - fixed crash in Postscript plug-in (bug #353381)
  - fixed handling of TABs in the text tool (bug #353132)
  - fixed bug in Depth Merge plug-in (bug #355219)
  - fixed bug in GimpDrawablePreview widget (bug #353639)
  - fixed bug in Line Nove script (bug #357433)
  - fixed bug in Ripple plug-in (bug #357431)
  - save locale independent files from Fractal Explorer plug-in (bug #360095)
  - fixed bug in Super Nova plug-in (bug #340073)
  - be more robust against broken XCF files (bug #357809)
  - fixed drawing issues in Image Map plug-in (bug #311621)
  - fixed smoothing option in Fractal Explorer plug-in (bug #372671)
  - load channels in the proper order when opening an XCF file (bug #378003)
  - deal with floating selections in the Burn-In Animation script (bug #384096)
  - fixed clipping in the GimpPreviewArea widget (bug #392692)
  - fixed a potential crash in gimp-remote (bug #392111)
  - work around a file-chooser problem on Windows (bug #398726)
  - fixed markup of the gimp(1) manual page (bug #401145)
  - fixed the fix for the right-to-left layout in layers dialog (bug #348347)
  - fixed PSD save plug-in on 64bit architectures (bug #335130)
  - added missing dependency in gimpui-2.0.pc file (bug #356394)
  - fixed a crash in the PSD save plug-in (bug #395385)
  - improved robustness of transform tool preview code (bug #420595)
  - improved forward compatibility of XCF loader (bug #316207)
  - don't crash in the Compressor plug-in if files can't be opened (bug #422444)
  - fixed sensitivity of input fields in the Lighting plug-in (bug #359833)

- don't BuildRequire gimp-print/gutenprint anymore

* Mon Mar 26 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.13-3
- use gutenprint per default for current development/future distribution
  versions (Fedora >= 7, RHEL >= 6)

* Mon Mar 26 2007 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.13-2
- own used directories in gimp-devel (#233794)

* Wed Feb 21 2007 Nils Philippsen <nphilipp@redhat.com>
- s/%%redhat/%%rhel/g

* Wed Feb 07 2007 Nils Philippsen <nphilipp@redhat.com>
- really change defaults for use of modular X and lcms (#224156)

* Thu Feb 01 2007 Nils Philippsen <nphilipp@redhat.com>
- change defaults for use of modular X and lcms (#224156)

* Fri Aug 25 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.13-1
- version 2.2.13
- remove obsolete filename patch

* Thu Aug 17 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.12-5
- don't barf on empty /etc/gimp/plugins.d (#202808)

* Wed Aug 16 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.12-4
- revamp scheme for integrating external plugins (#202545)

* Wed Aug 02 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.12-3
- allow spaces in filenames when saving (#200888, patch by Michael Natterer)

* Tue Jul 18 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.12-2
- split off libraries into gimp-libs to allow multilib installations
- remove pre-release cruft

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.12-1.1
- rebuild

* Mon Jul 10 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.12-1
- version 2.2.12
- use %%dist/%%fedora/%%redhat
- remove obsolete gcc4, libpng patches
- show build options in %%prep
- require gettext for building

* Wed May 31 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.11-5
- cope with pygobject2/-devel being split off (#193368)

* Tue May 09 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.11-4
- don't use long deprecated libpng API (#191027, patch by Manish Singh)

* Thu Apr 20 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.11-3
- only use pkgconfig if needed in gimptool, require pkgconfig in devel
  subpackage (#189314, #189371)

* Wed Apr 19 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.11-2
- require pkgconfig (#189314)

* Tue Apr 18 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.11-1
- version 2.2.11

* Fri Mar 03 2006 Nils Philippsen <nphilipp@redhat.com> - 2:2.2.10-4
- use htmlview as default web browser (#183730, patch by Ben Levenson)
- require hicolor-icon-theme (#182784, #182785)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.10-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.10-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Nils Philippsen <nphilipp@redhat.com>
- rebuild with lcms

* Thu Dec 29 2005 Nils Philippsen <nphilipp@redhat.com> - 2.2.10
- version 2.2.10

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 09 2005 Nils Philippsen <nphilipp@redhat.com>
- build with -fomit-frame-pointer to let assembly build with gcc 4.1

* Fri Dec 02 2005 Nils Philippsen <nphilipp@redhat.com>
- build with gcc 4.1

* Tue Nov 08 2005 Nils Philippsen <nphilipp@redhat.com>
- don't include .la files (#172626)
- require findutils for building

* Wed Nov 02 2005 Nils Philippsen <nphilipp@redhat.com> - 2.2.9
- version 2.2.9
- first attempt at dealing with modular X

* Tue Aug 16 2005 Nils Philippsen <nphilipp@redhat.com>
- rebuild

* Thu Jul 28 2005 Nils Philippsen <nphilipp@redhat.com>
- fix gimptool manpage symlink

* Mon Jul 25 2005 Nils Philippsen <nphilipp@redhat.com> - 2.2.8
- version 2.2.8
- clean up file list generation a bit
- gimptool manpage is in section 1 not 5
- list auto-generated .pyc and .pyo files

* Fri May 13 2005 Nils Philippsen <nphilipp@redhat.com>
- fix inline asm of MMX/SSE optimizations instead of using -mmmx and the like

* Fri May 13 2005 Nils Philippsen <nphilipp@redhat.com>
- fix cpuinstructionset patch so that it actually uses CPU-specific
  optimizations

* Wed May 11 2005 Nils Philippsen <nphilipp@redhat.com>
- use -mmmx/sse/sse2/... only for the relevant source files so that extended
  instruction sets only get used on suitable CPUs (#157409)

* Mon May 09 2005 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.7, fixes bug in SSE2 assembly for Lighten Only layer mode
  (#145771) and various other bugs
- on x86 and x86_64, use -msse and -msse2 to accomodate newer compilers

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 2:2.2.6-2
- silence %%post

* Mon Apr 11 2005 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.6

* Tue Mar 29 2005 Nils Philippsen <nphilipp@redhat.com>
- revert gtk requirement change

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com>
- Rebuild against newer libexif

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com>
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 22 2005 Nils Philippsen <nphilipp@redhat.com>
- install convenience symlinks for man pages

* Fri Mar 11 2005 Nils Philippsen <nphilipp@redhat.com>
- don't refer to freefonts and sharefonts in %%description

* Wed Mar 09 2005 Nils Philippsen <nphilipp@redhat.com>
- prevent gifload plugin from crashing when loading files with bogus frame size
  (#150677, #150678)

* Wed Mar 02 2005 Nils Philippsen <nphilipp@redhat.com>
- don't barf when building with gcc 4.0

* Wed Feb 23 2005 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.4
- require newer versions of gtk2 (#143840), glib2 and pango

* Sat Jan 29 2005 Nils Philippsen <nphilipp@redhat.com>
- make desktop icon themeable (#146486)

* Mon Jan 24 2005 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.3
- remove exifmarkerlength patch (improved version applied upstream)

* Mon Jan 17 2005 Nils Philippsen <nphilipp@redhat.com>
- clip thumbnail quality at 75 and don't barf on saving images at quality 0
  (fix patch for #145100)

* Fri Jan 14 2005 Nils Philippsen <nphilipp@redhat.com>
- avoid writing excessively long EXIF markers (#145100)

* Tue Jan 11 2005 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.2
- autogenerate %%microver

* Wed Dec 29 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.1
- pygimp-logo.png included in tarball again

* Mon Dec 20 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.2.0
- include pygimp-logo.png missing from tarball

* Fri Dec 10 2004 Nils Philippsen <nphilipp@redhat.com>
- use xsane plugin (un)install script if available

* Mon Nov 22 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.2-pre2

* Thu Nov 18 2004 Nils Philippsen <nphilipp@redhat.com>
- obsolete fixed gimp-perl version to be able to reintroduce it at a
  later point
- use correct dir in source URL

* Wed Nov 03 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.2-pre1

* Sun Oct 24 2004 Nils Philippsen <nphilipp@redhat.com>
- remove unnecessary echo statement

* Fri Oct 15 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.1.7 unstable

* Thu Oct 14 2004 Nils Philippsen <nphilipp@redhat.com>
- catch wrong values of bpp in BMP plugin (#135675), don't forget 1bpp and
  24bpp (d'oh)

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com>
- PreReq desktop-file-utils >= 0.9

* Sun Sep 26 2004 Nils Philippsen <nphilipp@redhat.com>
- fix post/postun requirements

* Sat Sep 25 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.5

* Thu Sep 16 2004 Nils Philippsen <nphilipp@redhat.com>
- rename desktop title (#132548)

* Thu Aug 26 2004 Nils Philippsen <nphilipp@redhat.com>
- add MimeType to desktop file
- run update-desktop-database in %%post/%%postun
- don't make stunts with -32 or -64 postfixed binaries anymore
- require /sbin/ldconfig and /usr/bin/update-desktop-database

* Tue Aug 10 2004 Nils Philippsen <nphilipp@redhat.com>
- build requires libwmf-devel

* Fri Aug 06 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.4

* Wed Aug 04 2004 Nils Philippsen <nphilipp@redhat.com>
- rebuild to pick up new libcroco

* Thu Jul 22 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.3
- buildreq gtk2-devel >= 2.4.0
- use -32 or -64 postfixed binaries if available

* Fri Jul 02 2004 Nils Philippsen <nphilipp@redhat.com>
- use included desktop (#126723), application-registry, mime-info and
  icon files
- remove perl cruft (Gimp-Perl is an external package now)
- further spec file cleaning

* Thu Jun 24 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.2
- fix summary (#126682)

* Tue Jun 22 2004 Nils Philippsen <nphilipp@redhat.com>
- build with gcc34 patch (sopwith)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Nils Philippsen <nphilipp@redhat.com>
- rebuild for Rawhide

* Wed May 26 2004 Nils Philippsen <nphilipp@redhat.com>
- add libjpeg-devel to BuildRequires (#121236)
- spit out slightly more informative help message if gimp-help is missing
  (#124307)

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com>
- rebuild

* Wed Apr 21 2004 Seth Nickell <snickell@redhat.com>
- Rename menu entry for .desktop file to "GIMP Image Editor"

* Tue Apr 20 2004 Nils Philippsen <nphilipp@redhat.com>
- update BuildRequires/Requires (#121236)

* Wed Apr 14 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.1

* Sun Mar 28 2004 Nils Philippsen <nphilipp@redhat.com>
- fix slide script-fu

* Sat Mar 27 2004 Nils Philippsen <nphilipp@redhat.com>
- bump some Build/Requires: versions
- change desktop file to actually run gimp-2.0

* Wed Mar 24 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.0

* Tue Mar 23 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0rc1

* Wed Mar 17 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0pre4

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com>
- Added epoch to gimp-perl obsoletes tag.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Nils Philippsen <nphilipp@redhat.com>
- fix typo in %%_enable_print macro
- install convenience symlinks (gimp, gimp-remote, gimptool)

* Sun Feb 08 2004 Nils Philippsen <nphilipp@redhat.com>
- require gtk2, glib2 >= 2.3.0, pango >= 1.3.0

* Fri Feb 06 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0pre3
- update buildroot patch
- enable building static libs (old default)
- have '--define'able enable_*
- disable building of print plugin, it's in another package

* Fri Jan 30 2004 Nils Philippsen <nphilipp@redhat.com>
- rebuild against new libcroco

* Sat Jan 24 2004 Nils Philippsen <nphilipp@redhat.com>
- require %%{epoch}:%%{version}-%%{release} of base package in sub packages
- rather use %%{?smp_mflags} to actually exploit SMP build systems

* Fri Jan 23 2004 Nils Philippsen <nphilipp@redhat.com>
- set epoch to 1 to upgrade old gimp rpms
- obsolete gimp2-devel, gimp-beta-devel to allow upgrade of 3rd party repo
  packages, gimp-perl to upgrade old package

* Fri Jan 23 2004 Nils Philippsen <nphilipp@redhat.com>
- fix binary name in desktop file ("gimp-1.3" until gimp-2.0 becomes final, to
  allow coexistence with old gimp-1.x packages)
- system intltool buildrequires perl-XML-Parser, work around that, yay

* Thu Jan 22 2004 Nils Philippsen <nphilipp@redhat.com>
- build as gimp, not gimp-beta
- remove all the beta blurbs
- fix automake dependency
- fix libtool usage

* Tue Jan 20 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0pre2

* Sun Jan 11 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0pre1

* Tue Nov 25 2003 Nils Philippsen <nphilipp@redhat.com>
- version 1.3.23 beta

* Fri Nov 21 2003 Nils Philippsen <nphilipp@redhat.com>
- version 1.3.22 beta

* Thu Oct 16 2003 Nils Philippsen <nphilipp@redhat.com>
- leave gtk-doc documentation in place
- move gimptool to main package
- own some directories previously not owned

* Tue Oct 07 2003 Nils Philippsen <nphilipp@redhat.com>
- version 1.3.21 beta

* Thu Sep 11 2003 Nils Philippsen <nphilipp@redhat.com>
- version 1.3.20 beta

* Mon Aug 11 2003 Nils Philippsen <nphilipp@redhat.com>
- version 1.3.18 beta

* Thu Jul 10 2003 Nils Philippsen <nphilipp@redhat.com>
- don't specify file modes with defattr

* Wed Jul 09 2003 Nils Philippsen <nphilipp@redhat.com>
- use system libtool

* Fri Jul 04 2003 Nils Philippsen <nils@redhat.de>
- version 1.3.16 beta
- update buildroot patch

* Tue Mar 25 2003 Nils Philippsen <nils@lisas.de>
- version 1.3.13 beta
- use automake-1.7

* Tue Feb 18 2003 Nils Philippsen <nils@lisas.de>
- version 1.3.12 beta

* Fri Oct 25 2002 Nils Philippsen <nils@lisas.de>
- version 1.3.9 beta
- move desktop file to /usr/share/applications

* Wed Aug 28 2002 Nils Philippsen <nils@redhat.de>
- version 1.3.8 beta
- update and fix buildroot patch, don't run automake/autoconf

* Mon Jul 08 2002 Nils Philippsen <nils@redhat.de>
- version 1.3.7 beta
- use automake 1.5 and autoconf 2.53

* Fri Mar 15 2002 Nils Philippsen <nils@redhat.de>
- version 1.3.4 beta

* Thu Jul 19 2001 Tim Powers <timp@redhat.com>
- remove the perl temp files to pacify rpmlint

* Tue Jun 19 2001 Matt Wilson <msw@redhat.com>
- added versioned requires to gimp-devel and gimp-perl

* Tue Apr  3 2001 Matt Wilson <msw@redhat.com>
- added gimp-1.2.1-locale.patch, which I've checked in to gimp CVS, to
  correctly set up the locale in plug-ins (#34214)

* Mon Apr  2 2001 Preston Brown <pbrown@redhat.com>
- some gimp-perl files weren't defattr'd (#34325)

* Fri Mar 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Don't include embedxpm, as it depends on a non-included perl module (#=33249)
- move gimpdoc and xcftopnm to gimp-perl, as they are dependant on the perl Gimp
  module

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Rebuild for GTK+-1.2.9 include paths

* Mon Jan 22 2001 Matt Wilson <msw@redhat.com>
- 1.2.1

* Mon Dec 25 2000 Matt Wilson <msw@redhat.com>
- 1.2.0

* Wed Dec 20 2000 Matt Wilson <msw@redhat.com>
- 1.1.31

* Thu Dec 14 2000 Matt Wilson <msw@redhat.com>
- 1.1.30
- merge changes from CVS into rpm-4.0 style spec file
- removed va_arg patch

* Mon Aug 21 2000 Matt Wilson <msw@redhat.com>
- 1.1.25

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Tue Aug  8 2000 Matt Wilson <msw@redhat.com>
- fixed directory mode on %%{_defaultdocdir}/gimp-%%{version}

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuild against new libpng

* Mon Jul 31 2000 Matt Wilson <msw@redhat.com>
- muck with modules filelist generation to avoid getting files owned by
  two packages

* Mon Jul 17 2000 Matt Wilson <msw@redhat.com>
- disable aa plugin
- moved the group back to Applications/Multimedia
- added desktop entry back into the file list

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  1 2000 Matt Wilson <msw@redhat.com>
- 1.1.24

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- use root, not bin for the default owner.

* Fri Jun 16 2000 Preston Brown <pbrown@redhat.com>
- add back missing system .desktop entry

* Sat Jun 10 2000 Matt Wilson <msw@redhat.com>
- rebuilt against fixed gcc

* Mon Jun  5 2000 Matt Wilson <msw@redhat.com>
- defattr for gimp-perl

* Sun Jun  4 2000 Matt Wilson <msw@redhat.com>
- drop out all of \.a$ from the main package list

* Sat Jun  3 2000 Matt Wilson <msw@redhat.com>
- 1.1.23
- use __NO_MATH_INLINES for now on ix86
- massive FHS surgery

* Tue May 16 2000 Matt Wilson <msw@redhat.com>
- 1.1.22

* Mon Apr 24 2000 Matt Wilson <msw@redhat.com>
- 1.1.20

* Fri Apr 14 2000 Matt Wilson <msw@redhat.com>
- include subdirs in the help find
- remove gimp-help-files generation
- both gimp and gimp-perl own prefix/lib/gimp/1.1/plug-ins
- both gimp and gimp-devel own prefix/lib/gimp/1.1/modules

* Thu Apr 13 2000 Matt Wilson <msw@redhat.com>
- 1.1.19
- get all .mo files

* Wed Jan 19 2000 Gregory McLean <gregm@comstar.net>
- Version 1.1.15

* Wed Dec 22 1999 Gregory McLean <gregm@comstar.net>
- Version 1.1.14
- Added some auto %%files section generation scriptlets
