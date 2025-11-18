#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg basket
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0.3.1
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Taking care of your ideas
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/office/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-tdepim-devel >= %{tde_version}
BuildRequires:	trinity-kontact-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	gpgme-devel

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	libtool

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
This application is mainly an all-purpose notes taker. It provide several baskets where
to drop every sort of items: text, rich text, links, images, sounds, files, colors,
application launcher... Objects can be edited, copied, dragged... So, you can arrange
them as you want ! This application can be used to quickly drop web objects (link, text,
images...) or notes, as well as to free your clutered desktop (if any). It is also useful
to collect informations for a report. Those data can be shared with co-workers by exporting
baskets to HTML.

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INCLUDE_PATH="%{tde_tdeincludedir}" \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  \
  -DBUILD_ALL=ON \
  -DWITH_ALL_OPTIONS="ON" \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -G "Extended Clipboard" "%{?buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop" DesktopUtility
%endif

# Apps that should stay in TDE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop"


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/basket
%{tde_tdeappdir}/basket.desktop
%{tde_datadir}/apps/basket/
%dir %{tde_datadir}/apps/kontact/ksettingsdialog
%{tde_datadir}/apps/kontact/ksettingsdialog/kontact_basketplugin.setdlg
%{tde_libdir}/libbasketcommon.la
%{tde_libdir}/libbasketcommon.so
%{tde_tdelibdir}/basketthumbcreator.la
%{tde_tdelibdir}/basketthumbcreator.so
%{tde_tdelibdir}/kcm_basket.la
%{tde_tdelibdir}/kcm_basket.so
%{tde_tdelibdir}/libbasketpart.la
%{tde_tdelibdir}/libbasketpart.so
%{tde_tdelibdir}/libkontact_basket.la
%{tde_tdelibdir}/libkontact_basket.so
%config(noreplace) %{tde_confdir}/magic/basket.magic
%{tde_datadir}/icons/crystalsvg/*/*/*
%{tde_datadir}/mimelnk/application/x-basket-archive.desktop
%{tde_datadir}/mimelnk/application/x-basket-template.desktop
%{tde_datadir}/services/basket_config_apps.desktop
%{tde_datadir}/services/basket_config_baskets.desktop
%{tde_datadir}/services/basket_config_general.desktop
%{tde_datadir}/services/basket_config_new_notes.desktop
%{tde_datadir}/services/basket_config_notes_appearance.desktop
%{tde_datadir}/services/basket_part.desktop
%{tde_datadir}/services/basketthumbcreator.desktop
%{tde_datadir}/services/kontact/basket.desktop
%{tde_tdedocdir}/HTML/en/basket/
%config(noreplace) %{tde_confdir}/magic/basket.magic.mgc
%{tde_mandir}/man1/basket.*

