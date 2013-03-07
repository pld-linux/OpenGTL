#
%bcond_with	tests
#
Summary:	Graphics Transformation Languages
Name:		OpenGTL
Version:	0.9.18
Release:	0.1
License:	LGPLv2
Group:		Libraries
URL:		http://opengtl.org/
Source0:	http://download.opengtl.org/%{name}-%{version}.tar.bz2
# Source0-md5:	8a9673c648ef5af4fcc7f60bb8282811
%{?with_tests:Source1:	http://download.opengtl.org/tests-data-%{version}.tar.bz2}
BuildRequires:	ImageMagick
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	libpng-devel
BuildRequires:	llvm-devel >= 3.0
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}

%description
OpenGTL provides tools, languages and libraries to create generic
transformations for graphics. These transformations can be used by
different programs, e.g. Krita, Gimp, CinePaint, etc.

%package libs
######		Unknown group!
Summary:	Runtime libraries for %{name}
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}

%description libs
OpenGTL libraries.

%package devel
Summary:	Libraries and header files for %{name}
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Requires:	llvm-devel

%description devel
This package contains library and header files needed to develop new
native programs that use the OpenGTL libraries.

%prep
%setup -q %{?with_tests:-a1}

%build
install -d build
cd build
%cmake \
  -DOPENGTL_BUILD_TESTS:BOOL=ON \
  %{?with_tests:-DOPENGTL_TESTS_DATA:PATH=$PWD/../tests-data} \
  ..

%{__make}

cd ..
doxygen OpenGTL.doxy

%if %{with tests}
export PKG_CONFIG_PATH=$RPM_BUILD_ROOT%{_npkgconfigdir}:%{buildroot}%{_pkgconfigdir}
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

## unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/OpenGTL

%clean
rm -rf $RPM_BUILD_ROOT

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

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(644,root,root,755)
%{_libdir}/libGTLCore.so.%{version}
%{_libdir}/libGTLFragment.so.%{version}
%{_libdir}/libGTLImageIO.so.%{version}
%{_libdir}/libOpenCTL.so.%{version}
%{_libdir}/libOpenShiva.so.%{version}
%{_libdir}/libGTLCore.so.0.8
%{_libdir}/libGTLFragment.so.0.8
%{_libdir}/libGTLImageIO.so.0.8
%{_libdir}/libOpenCTL.so.0.8
%{_libdir}/libOpenShiva.so.0.8
%{_libdir}/GTLImageIO

%files devel
%defattr(644,root,root,755)
%doc html/* build/OpenShiva/doc/reference/ShivaRef.pdf
%attr(755,root,root) %{_bindir}/ctlc
%attr(755,root,root) %{_bindir}/shivac
%attr(755,root,root) %{_bindir}/shivatester
%{_includedir}/GTLCore
%{_includedir}/GTLFragment
%{_includedir}/GTLImageIO
%{_includedir}/OpenCTL
%{_includedir}/OpenShiva
%{_libdir}/libGTLCore.so
%{_libdir}/libGTLFragment.so
%{_libdir}/libGTLImageIO.so
%{_libdir}/libOpenCTL.so
%{_libdir}/libOpenShiva.so
%{_pkgconfigdir}/GTLCore.pc
%{_pkgconfigdir}/GTLImageIO.pc
%{_pkgconfigdir}/OpenCTL.pc
%{_pkgconfigdir}/OpenShiva.pc
