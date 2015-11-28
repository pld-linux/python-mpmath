#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A pure Python library for multiprecision floating-point arithmetic
Name:		python-mpmath
Version:	0.18
Release:	5
License:	BSD
Group:		Libraries/Python
URL:		http://code.google.com/p/mpmath/
Source0:	http://mpmath.googlecode.com/files/mpmath-%{version}.tar.gz
# Source0-md5:	e2e7a7932969f52f25b7e19d8f0438bd
Source1:	http://mpmath.googlecode.com/files/mpmath-docsrc-%{version}.tar.gz
# Source1-md5:	65286d76dff4f02f41b31f1c3d1810dd
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-Sphinx
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python-Sphinx
%endif
BuildRequires:	texlive-latex
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mpmath is a pure-Python library for multiprecision floating-point
arithmetic. It provides an extensive set of transcendental functions,
unlimited exponent sizes, complex numbers, interval arithmetic,
numerical integration and differentiation, root-finding, linear
algebra, and much more. Almost any calculation can be performed just
as well at 10-digit or 1000-digit precision, and in many cases mpmath
implements asymptotically fast algorithms that scale well for
extremely high precision work. If available, mpmath will (optionally)
use gmpy to speed up high precision operations.

If you require plotting capabilities in mpmath, install
python-matplotlib.

%package -n python3-mpmath
Summary:	A pure Python library for multiprecision floating-point arithmetic
Group:		Libraries/Python

%description -n python3-mpmath
Mpmath is a pure-Python library for multiprecision floating-point
arithmetic. It provides an extensive set of transcendental functions,
unlimited exponent sizes, complex numbers, interval arithmetic,
numerical integration and differentiation, root-finding, linear
algebra, and much more. Almost any calculation can be performed just
as well at 10-digit or 1000-digit precision, and in many cases mpmath
implements asymptotically fast algorithms that scale well for
extremely high precision work. If available, mpmath will (optionally)
use gmpy to speed up high precision operations.

If you require plotting capabilities in mpmath, install
python3-matplotlib.

%package doc
Summary:	HTML documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the HTML documentation for %{name}.

%prep
%setup -q -n mpmath-%{version} -a 1
# Convert line encodings
for doc in LICENSE CHANGES PKG-INFO README.rst mpmath/tests/runtests.py; do
	%{__sed} "s|\r||g" $doc > $doc.new && \
		touch -r $doc $doc.new && \
		%{__mv} $doc.new $doc
done
find doc -name *.txt -exec sed -i "s|\r||g" {} \;

shebangs="mpmath/matrices/eigen.py mpmath/matrices/eigen_symmetric.py mpmath/tests/runtests.py mpmath/tests/test_eigen.py mpmath/tests/test_eigen_symmetric.py mpmath/tests/test_levin.py"
# Get rid of unnecessary shebangs
for lib in $shebangs; do
	%{__sed} '/^#!.*/d; 1q' $lib > $lib.new && \
		touch -r $lib $lib.new && \
		%{__mv} $lib.new $lib
done

%build
%if %{with python2}
%py_build
%py_build
%endif

%if %{with python3}
%py3_build
%endif

cd doc
python build.py

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README.rst
%{py_sitescriptdir}/mpmath/
%{py_sitescriptdir}/mpmath-%{version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-mpmath
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README.rst
%{py3_sitescriptdir}/mpmath/
%{py3_sitescriptdir}/mpmath-%{version}-*.egg-info
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/build/*
