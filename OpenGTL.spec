#
# Conditional build:
%bcond_with	tests		# perform "make test"
#
Summary:	Graphics Transformation Languages
Summary(pl.UTF-8):	Graphics Transformation Languages - języki przekształceń graficznych
Name:		OpenGTL
Version:	0.9.18
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://download.opengtl.org/%{name}-%{version}.tar.bz2
# Source0-md5:	8a9673c648ef5af4fcc7f60bb8282811
%{?with_tests:Source1:	http://download.opengtl.org/tests-data-%{version}.tar.bz2}
Patch0:		%{name}-llvm-3.3.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-link.patch
URL:		http://opengtl.org/
BuildRequires:	ImageMagick
BuildRequires:	cmake >= 2.6
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	libpng-devel
BuildRequires:	llvm-devel >= 3.3
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
BuildRequires:	texlive-makeindex
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGTL provides tools, languages and libraries to create generic
transformations for graphics. These transformations can be used by
different programs, e.g. Krita, Gimp, CinePaint, etc.

%description -l pl.UTF-8
OpenGTL udostępnia narzędzia, języki i biblioteka do tworzenia
ogólnych przekształceń grafiki. Przekształcenia te mogą być później
wykorzystywane przez różne programy, takie jak Krita, Gimp czy
CinePaint.

%package libs
Summary:	Runtime OpenGTL libraries
Summary(pl.UTF-8):	Biblioteki współdzielone OpenGTL
Group:		Libraries

%description libs
OpenGTL shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone OpenGTL.

%package devel
Summary:	Header files for OpenGTL
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGTL
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Requires:	llvm-devel >= 3.3

%description devel
This package contains the header files needed to develop new native
programs that use the OpenGTL libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe niezbędne do tworzenia nowych
programów wykorzystujących biblioteki OpenGTL.

%prep
%setup -q %{?with_tests:-a1}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DOPENGTL_BUILD_OpenRIJN:BOOL=ON \
	-DOPENGTL_BUILD_TESTS:BOOL=ON \
	%{?with_tests:-DOPENGTL_TESTS_DATA:PATH=$PWD/../tests-data}

%{__make}

cd ..
doxygen OpenGTL.doxy

%if %{with tests}
export PKG_CONFIG_PATH=$RPM_BUILD_ROOT%{_npkgconfigdir}:$RPM_BUILD_ROOT%{_pkgconfigdir}
test "$(pkg-config --modversion GTLCore)" = "%{version}"
test "$(pkg-config --modversion GTLImageIO)" = "%{version}"
test "$(pkg-config --modversion OpenCTL)" = "%{version}"
test "$(pkg-config --modversion OpenShiva)" = "%{version}"
# some known failures due to missing test data , 17 tests failed out of 189
# *with* test data, down to 2:
# The following tests FAILED:
#		177 - PerlinNoise.shiva (Failed)
#		189 - grayscaliser.shiva (Failed)
%{__make} test -C  %{_target_platform} ||:
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/OpenGTL

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING OpenGTL/README
%attr(755,root,root) %{_bindir}/ctli
%attr(755,root,root) %{_bindir}/ctltc
%attr(755,root,root) %{_bindir}/gtlconvert
%attr(755,root,root) %{_bindir}/imagecompare
%attr(755,root,root) %{_bindir}/shiva
%attr(755,root,root) %{_bindir}/shivacheck
%attr(755,root,root) %{_bindir}/shivainfo
%attr(755,root,root) %{_bindir}/shivanimator
%{_datadir}/OpenGTL

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGTLCore.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libGTLCore.so.0.8
%attr(755,root,root) %{_libdir}/libGTLFragment.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libGTLFragment.so.0.8
%attr(755,root,root) %{_libdir}/libGTLImageIO.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libGTLImageIO.so.0.8
%attr(755,root,root) %{_libdir}/libOpenCTL.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libOpenCTL.so.0.8
%attr(755,root,root) %{_libdir}/libOpenShiva.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libOpenShiva.so.0.8
%dir %{_libdir}/GTLImageIO
%dir %{_libdir}/GTLImageIO/Extensions
%attr(755,root,root) %{_libdir}/GTLImageIO/Extensions/lib*.so

%files devel
%defattr(644,root,root,755)
%doc html/* build/OpenShiva/doc/reference/ShivaRef.pdf
%attr(755,root,root) %{_bindir}/ctlc
%attr(755,root,root) %{_bindir}/shivac
%attr(755,root,root) %{_bindir}/shivatester
%attr(755,root,root) %{_libdir}/libGTLCore.so
%attr(755,root,root) %{_libdir}/libGTLFragment.so
%attr(755,root,root) %{_libdir}/libGTLImageIO.so
%attr(755,root,root) %{_libdir}/libOpenCTL.so
%attr(755,root,root) %{_libdir}/libOpenShiva.so
%{_includedir}/GTLCore
%{_includedir}/GTLFragment
%{_includedir}/GTLImageIO
%{_includedir}/OpenCTL
%{_includedir}/OpenShiva
%{_pkgconfigdir}/GTLCore.pc
%{_pkgconfigdir}/GTLImageIO.pc
%{_pkgconfigdir}/OpenCTL.pc
%{_pkgconfigdir}/OpenShiva.pc
