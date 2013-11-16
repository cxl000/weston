%define with-cairo yes
Name:           weston
Version:        1.3.0
Release:        1
Summary:        Wayland Compositor Infrastructure
License:        MIT
Group:          System/GUI/Other
Url:            http://weston.freedesktop.org/
Source:         %name-%version.tar.xz
Patch1:         000_simple_clients_programs_LDADD.patch
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(expat)
BuildRequires:  libjpeg-devel
#BuildRequires:  libvpx-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
#BuildRequires:  rsvg-view
BuildRequires:	xkeyboard-config
%if "%{with-cairo}" == "yes"
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-egl) >= 1.11.3
BuildRequires:	pkgconfig(cairo-xcb)
%endif
BuildRequires:  pkgconfig(egl) >= 7.10
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
#BuildRequires:  gfx-rpi-libGLESv2-devel
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libdrm) >= 2.4.30
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(libudev) >= 136
BuildRequires:  pkgconfig(mtdev) >= 1.1.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(wayland-client) >= 1.0.0
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:  pkgconfig(xkbcommon) >= 0.0.578
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcursor)
Requires:	xkeyboard-config

%description
Weston is the reference implementation of a Wayland compositor, and a
useful compositor in its own right. Weston has various backends that
lets it run on Linux kernel modesetting and evdev input as well as
under X11. Weston ships with a few example clients, from simple
clients that demonstrate certain aspects of the protocol to more
complete clients and a simplistic toolkit. There is also a quite
capable terminal emulator (weston-terminal) and an toy/example
desktop shell. Finally, weston also provides integration with the
Xorg server and can pull X clients into the Wayland desktop and act
as a X window manager.

%package devel
Summary:    Weston SDK
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Weston SDK files

%prep
%setup -q
%patch1 -p1

%build
cd weston
%reconfigure \
           --disable-static \
           --enable-tablet-shell \
           --enable-xwayland \
           --enable-x11-compositor \
           --enable-drm-compositor \
           --enable-wayland-compositor \
           --enable-fbdev-compositor \
           --disable-rdp-compositor \
           --enable-weston-launch \
%if "%{with-cairo}" == "yes"
           --with-cairo-glesv2 \
%endif
           --enable-simple-clients \
           --enable-simple-egl-clients \
           --enable-clients \
           --enable-demo-clients=yes \
           --disable-colord \
           --disable-setuid-install
make %{?_smp_mflags};

%install
cd weston
make install DESTDIR="%buildroot";
rm -f "%buildroot/%_libdir"/*.la "%buildroot/%_libdir/weston"/*.la;

%check
mkdir -pm go-rwx xdg;
# Ignore exit code, because """the headless backend is not even in the 1.0
# stable series. It means it will be an option starting from 1.2 of stable
# series."""
XDG_RUNTIME_DIR="$PWD/xdg" make check || :;

%files
%defattr(-,root,root)
%_bindir/wcap-*
%_bindir/weston*
%_libexecdir/weston-*
%_libdir/weston
%_datadir/weston
%_mandir/man1/weston.1*
%_mandir/man7/weston*7*


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/weston.pc
%doc %{_mandir}/man5/weston.ini.5.gz
# >> files devel
# << files devel

