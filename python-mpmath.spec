#
# Conditional build:
%bcond_without	doc	# HTML documentation
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

Summary:	A pure Python library for multiprecision floating-point arithmetic
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do arytmetyki zmiennoprzecinkowej wielokrotnej precyzji
Name:		python-mpmath
Version:	1.3.0
Release:	1
License:	BSD
Group:		Libraries/Python
# pypi release is missing docs and CHANGES
#Source0Download: https://pypi.org/simple/mpmath/
#Source0:	https://files.pythonhosted.org/packages/source/m/mpmath/mpmath-%{version}.tar.gz
## Source0-md5:	d5d17bbefea73eeb959967351d905306
# ... so use github
#Source0Download: https://github.com/fredrik-johansson/mpmath/releases
Source0:	https://github.com/fredrik-johansson/mpmath/archive/%{version}/mpmath-%{version}.tar.gz
# Source0-md5:	63376989afeb861a729bbf14ae6cb7bc
URL:		https://mpmath.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 1:36.7.0
BuildRequires:	python-setuptools_scm >= 1.7.0
%if %{with tests}
BuildRequires:	python-pytest >= 4.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 1:36.7.0
BuildRequires:	python3-setuptools_scm >= 1.7.0
%if %{with tests}
BuildRequires:	python3-pytest >= 4.6
%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python-modules >= 1:2.7
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

%description -l pl.UTF-8
Mpmath to czysto pythonowa biblioteka do arytmetyki
zmiennoprzecinkowej wielokrotnej precyzji. Zapewnia obszerny zbiór
funkcji przestępnych, nieograniczone rozmiary wykładnika, liczby
zespolone, arytmetykę na przedziałach, całkowanie i różniczkowanie
numeryczne, szukanie pierwiastków, algebrę liniową itd. Można
wykonać prawie dowolne obliczenia, zarówno z 10-cyfrową, jak i
1000-cyfrową dokładnością, a dla wielu przypadków mpmath ma
zaimplementowane asymptotycznie szybkie algorytmy, dobrze skalujące
się dla bardzo dużej precyzji. Mpmath może opcjonalnie (jeśli jest
dostępny) używać modułu gmpy do przyspieszenia operacji.

Do obsługi wykresów w mpmath należy zainstalować pakiet
python-matplotlib.

%package -n python3-mpmath
Summary:	A pure Python library for multiprecision floating-point arithmetic
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do arytmetyki zmiennoprzecinkowej wielokrotnej precyzji
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

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

%description -n python3-mpmath -l pl.UTF-8
Mpmath to czysto pythonowa biblioteka do arytmetyki
zmiennoprzecinkowej wielokrotnej precyzji. Zapewnia obszerny zbiór
funkcji przestępnych, nieograniczone rozmiary wykładnika, liczby
zespolone, arytmetykę na przedziałach, całkowanie i różniczkowanie
numeryczne, szukanie pierwiastków, algebrę liniową itd. Można
wykonać prawie dowolne obliczenia, zarówno z 10-cyfrową, jak i
1000-cyfrową dokładnością, a dla wielu przypadków mpmath ma
zaimplementowane asymptotycznie szybkie algorytmy, dobrze skalujące
się dla bardzo dużej precyzji. Mpmath może opcjonalnie (jeśli jest
dostępny) używać modułu gmpy do przyspieszenia operacji.

Do obsługi wykresów w mpmath należy zainstalować pakiet
python3-matplotlib.

%package doc
Summary:	API documentation for mpmath module
Summary(pl.UTF-8):	Dokumentacja API modułu mpmath
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the HTML documentation for mpmath module.

%description doc -l pl.UTF-8
Ten pakiet zawiera dokumentację modułu mpmath w formacie HTML.

%prep
%setup -q -n mpmath-%{version}

shebangs="mpmath/matrices/eigen.py mpmath/matrices/eigen_symmetric.py mpmath/tests/test_eigen.py mpmath/tests/test_eigen_symmetric.py mpmath/tests/test_levin.py"
# Get rid of unnecessary shebangs
for lib in $shebangs; do
	%{__sed} '/^#!.*/d; 1q' $lib > $lib.new && \
		touch -r $lib $lib.new && \
		%{__mv} $lib.new $lib
done

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_axes uses DISPLAY
# test_convert.py::test_compatibility fails (on x86 only?) due to precision
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest -k 'not test_axes and not test_compatibility' mpmath/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -k 'not test_axes and not test_compatibility' mpmath/tests
%endif
%endif

%if %{with doc}
#cd doc
#install -d build
PYTHONPATH=$(pwd) \
sphinx-build-3 -E -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/mpmath/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/mpmath/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%{py_sitescriptdir}/mpmath
%{py_sitescriptdir}/mpmath-%{version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-mpmath
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%{py3_sitescriptdir}/mpmath
%{py3_sitescriptdir}/mpmath-%{version}-*.egg-info
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,calculus,functions,*.html,*.js}
%endif
