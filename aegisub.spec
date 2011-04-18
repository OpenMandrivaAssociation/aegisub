Summary:	Comprehensive video subtitle creation tool
Name:		aegisub
Version:	2.1.8
Release:	%mkrel 1
Source0:	http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.gz
Patch0:		aegisub-2.1.8-link.patch
Patch1:		aegisub-2.1.8-external-libass.patch
Patch5:		aegisub-2.1.8-wxexception.patch
URL:		http://www.aegisub.org/
License:	BSD
Group:		Video
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
BuildRequires:	pulseaudio-devel
BuildRequires:	libass-devel
BuildRequires:	libgomp-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
Aegisub is a powerful and comprehensive tool for creating subtitles
for video files.

%prep
%setup -qn %{name}-%{version}
%patch0 -p0 -b .link
%patch1 -p0 -b .ass
%patch5 -p0

%build
autoreconf -fi
export CXXFLAGS="%optflags -D__STDC_CONSTANT_MACROS"
%configure2_5x \
	--target=%_target_platform \
	--with-wx-config=wx-config-unicode \
	--with-external-libass \
	--without-lua50 \
	--without-openal \
	--without-portaudio \
	--without-perl \
	--without-ruby
%make

%install
rm -rf %buildroot}
%makeinstall_std

%find_lang %{name}21

%clean
rm -rf %{buildroot}

%files -f %{name}21.lang
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
