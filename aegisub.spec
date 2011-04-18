Summary:	Comprehensive video subtitle creation tool
Name:		aegisub
Version:	2.1.8
Release:	%mkrel 1
Source0:	http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.gz
# From upstream via Gentoo: http://bugs.gentoo.org/174191
Source1:	aegisub.png
Patch0:		aegisub-2.1.8-link.patch
# Fix disabling ffmpegsource (not needed for Cooker build, but what
# the hell, it doesn't hurt anything) - AdamW 2009/01
Patch1:		aegisub-2618-ffmpegdisable.patch
# Upstream configure tries to find out what svn revision it is, which
# means you'd have to keep all the SVN crap in the tarball and
# buildrequire subversion. So let's just patch it out and hardcode it:
# this patch sets it to an arbitrary string which is sed'ed out in
# prep - AdamW 2009/01
Patch2:		aegisub-2618-svnrev.patch
Patch5:		aegisub-2.1.8-wxexception.patch
URL:		http://www.aegisub.org/
License:	BSD
Group:		Video
# Upstream dependency reference: http://www.malakith.net/aegiwiki/Unix_Instructions
# but handle with care, it's not always updated - AdamW 2009/01
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	wxgtku-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	mesaglu-devel
BuildRequires:	freetype2-devel
BuildRequires:	libalsa-devel
BuildRequires:	lua-devel
BuildRequires:	fontconfig-devel
BuildRequires:	hunspell-devel
BuildRequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
Aegisub is a powerful and comprehensive tool for creating subtitles
for video files.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .link
%patch5 -p0

%build
autoreconf -fi
export CXXFLAGS="%optflags -D__STDC_CONSTANT_MACROS"
%configure2_5x \
	--enable-debug-exceptions \
	--with-wx-config=wx-config-unicode \
	--without-lua50 \
	--without-openal \
	--without-portaudio \
	--without-perl \
	--without-ruby
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Aegisub
Comment=Comprehensive video subtitle creation tool
Exec=soundwrapper %{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;AudioVideo;Video;Player;AudioVideoEditing;
EOF

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32}/apps
convert -scale 16x16 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 0644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
