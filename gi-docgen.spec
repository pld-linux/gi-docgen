#
# Conditional build:
%bcond_without	doc	# Sphinx documentation

Summary:	Documentation tool for GObject-based libraries
Summary(pl.UTF-8):	Narzędzie do dokumentowania bibliotek opartych na GObject
Name:		gi-docgen
Version:	2021.7
Release:	1
License:	Apache v2.0 or GPL v3+
Group:		Development/Tools
Source0:	https://download.gnome.org/sources/gi-docgen/2021/%{name}-%{version}.tar.xz
# Source0-md5:	fd045b8e3ccd1b1305e5e87afa728ac0
URL:		https://gitlab.gnome.org/GNOME/gi-docgen
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with doc}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-jinja2
BuildRequires:	python3-markdown
BuildRequires:	python3-markupsafe
BuildRequires:	python3-pygments
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-toml
BuildRequires:	python3-typogrify
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GI-Docgen is a document generator for GObject-based libraries. GObject
is the base type system of the GNOME project. GI-Docgen reuses the
introspection data generated by GObject-based libraries to generate
the API reference of these libraries, as well as other ancillary
documentation.

%description -l pl.UTF-8
GI-Docgen to generator dokumentacji do bibliotek opartych na
bibliotece GObject. GObject to bazowy system typów projektu GNOME.
GI-Docgen wykorzystuje dane introspekcji wygenerowane przez biblioteki
oparte na GObject w celu wygenerowania dokumentacji API bibliotek, a
także innej, dodatkowej dokumentacji.

%package doc
Summary:	Documentation for GI-Docgen tool
Summary(pl.UTF-8):	Dokumentacja do narzędzia GI-Docgen
Group:		Documentation

%description doc
Documentation for GI-Docgen tool.

%description doc -l pl.UTF-8
Dokumentacja do narzędzia GI-Docgen.

%prep
%setup -q

%build
%py3_build

%if %{with doc}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_npkgconfigdir}
cat >$RPM_BUILD_ROOT%{_npkgconfigdir}/gi-docgen.pc <<EOF
prefix=%{_prefix}
bindir=%{_bindir}

EOF

sed -e 's/@VERSION@/%{version}/' gi-docgen.pc.in >>$RPM_BUILD_ROOT%{_npkgconfigdir}/gi-docgen.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gi-docgen
%{py3_sitescriptdir}/gidocgen
%{py3_sitescriptdir}/gi_docgen-%{version}-py*.egg-info
%{_npkgconfigdir}/gi-docgen.pc
%{_mandir}/man1/gi-docgen.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/{_static,tools,*.html,*.js}
%endif
