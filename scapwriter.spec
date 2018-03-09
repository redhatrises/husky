%define _py python

Name:           scap-writer
Version:        0.1
Release:        1%{?dist}
Summary:        SCAP-Security-Guide IDE GUI
License:        GPLv3
URL:            https://github.com/redhatrises/husky.git
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{_py}
BuildRequires:  %{_py}-qt5
Requires:  %{_py}
Requires:  PyYAML
Requires:  %{_py}-qt5

%description
This is an IDE that allows easy development of SCAP content for the
SCAP-Security-Guide project.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
#%doc LICENSE ChangeLog README.md
%{python_sitelib}/*
%{_bindir}/scap-writer

%changelog
* Fri Sep 08 2017 Gabriel Alford <galford@redhat.com> -0.1-1
- Initial RPM for scapwriter
