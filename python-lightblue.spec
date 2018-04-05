%global srcname lightblue

Name:           python-lightblue
Version:        0.1.3
Release:        1%{?dist}
Summary:        A Python API for Lightblue database.

Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/Allda/python-lightblue
Source0:        https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-setuptools
BuildRequires:  python2-nose
BuildRequires:  python3-nose

BuildArch:      noarch

%description
A Python API for Lightblue database. https://lightblue.io

%package -n python2-%{srcname}
Summary:        %{Summary}

Requires:       python-dpath
Requires:       python2-beanbag

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Python API for Lightblue database.


%package -n python3-%{srcname}
Summary:        %{Summary}

Requires:       python3-dpath
Requires:       python3-beanbag

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Python API for Lightblue database.

%prep
%autosetup -n %{srcname}-%{version}
# do not use rednose during rpm build
sed -i 's/rednose/\#rednose/' setup.cfg

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
nosetests-%{python2_version}
nosetests-%{python3_version}


%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*


%changelog
