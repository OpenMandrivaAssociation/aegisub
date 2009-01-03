%define snap	2618
%define _disable_ld_no_undefined	1

Summary:	Comprehensive video subtitle creation tool
Name:		aegisub
Version:	2.1.6
Release:	%{mkrel 0.%{snap}.1}
# They don't seem to do stable release tarballs, so I'm not bothering
# to have a conditional for them yet. - AdamW 2009/01
Source0:	http://www.mahou.org/~verm/aegisub/%{name}-%{snap}.tar.lzma
# From upstream via Gentoo: http://bugs.gentoo.org/174191
Source1:	aegisub.png
# Fix underlinking - AdamW 2009/01
Patch0:		aegisub-2618-underlink.patch
# Fix disabling ffmpegsource (not needed for Cooker build, but what
# the hell, it doesn't hurt anything) - AdamW 2009/01
Patch1:		aegisub-2618-ffmpegdisable.patch
# Upstream configure tries to find out what svn revision it is, which
# means you'd have to keep all the SVN crap in the tarball and
# buildrequire subversion. So let's just patch it out and hardcode it:
# this patch sets it to an arbitrary string which is sed'ed out in
# prep - AdamW 2009/01
Patch2:		aegisub-2618-svnrev.patch
URL:		http://aegisub.cellosoft.com
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
%setup -q -n %{name}
%patch0 -p1 -b .underlink
%patch1 -p1 -b .ffmpeg
%patch2 -p1 -b .svnrev

# This goes along with svnrev.patch - AdamW 2009/01
sed -i -e 's,__MDV_SVN_REV,%{snap},g' configure.in

%build
# needed for underlink.patch, ffmpegdisable.patch and svnrev.patch
# - AdamW 2009/01
./autogen.sh

# According to upstream, there's no point in using the old auto3,
# since we have lua 5.1 for auto4 support. They also say that OpenAL,
# PortAudio and PulseAudio all don't work well, and recommend using
# the Alsa backend. They list Perl and Ruby scripting as both
# incomplete and unmaintained and say everyone just uses auto4.
# - AdamW 2009/01
%configure2_5x --with-wx-config=wx-config-unicode \
	--without-lua50 \
	--without-openal \
	--without-portaudio \
	--without-pulseaudio \
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
