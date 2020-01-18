%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-cffi
Version:        1.6.0
Release:        5%{?dist}
Summary:        Foreign Function Interface for Python to call C code
License:        MIT
URL:            http://cffi.readthedocs.org/
Source0:        https://pypi.io/packages/source/c/cffi/cffi-%{version}.tar.gz

BuildRequires:  libffi-devel python-sphinx
BuildRequires:  python-devel python-setuptools Cython python-pycparser
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-Cython python3-pycparser
%endif # if with_python3

Requires:       python-pycparser

# Do not check .so files in the python_sitelib directory
# or any files in the application's directory for provides
%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\\.so$

%description
Foreign Function Interface for Python, providing a convenient and
reliable way of calling existing C code from Python. The interface is
based on LuaJIT’s FFI.

%if 0%{?with_python3}
%package -n python3-cffi
Summary:        Foreign Function Interface for Python 3 to call C code
Requires:       python3-pycparser
%{?python_provide:%python_provide python3-cffi}

%description -n python3-cffi
Foreign Function Interface for Python, providing a convenient and
reliable way of calling existing C code from Python. The interface is
based on LuaJIT’s FFI.
%endif # with_python3

%package doc
Summary:        Documentation for CFFI
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for CFFI, the Foreign Function Interface for Python.

%prep
%setup -q -n cffi-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python} setup.py build
cd doc
make html
rm build/html/.buildinfo

#%check
## The following test procedure works when I run it manually, but fails
## from rpmbuild, complaining that it can't import _cffi_backend, and I'm
## not sure how to make it work
#python setup_base.py build
#PYTHONPATH=build/lib.linux-* py.test c/ testing/

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif # with_python3
%{__python} setup.py install \
    --skip-build --prefix=%{_prefix} --root %{buildroot} \
    --record %{buildroot}%{python_sitearch}/cffi-%{version}-py2.7.egg-info/installed-files.txt

%files
%doc PKG-INFO
%license LICENSE
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-cffi
%doc PKG-INFO
%license LICENSE
%{python3_sitearch}/*
%endif # with_python3

%files doc
%doc doc/build/html

%changelog
* Tue Aug 09 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.6.0-5
- Record installed files (#1255206)

* Tue May 03 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.6.0-4
- Import from Fedora
- Migrate python2-cffi => python-cffi

* Thu Apr 28 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6.0-3
- Switch Source0 to using pypi.io

* Thu Apr 28 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6.0-2
- Update Source0 URL to account for pypi change

* Thu Apr 21 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 (#1329203)

* Mon Feb 15 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (#1299272)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.5.0-1
- Update to 1.5.0 (#1299272)

* Mon Jan 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.4.2-2
- Move python-cffi => python2-cffi

* Tue Dec 22 2015 John Dulaney <jdulaney@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2 (#1293504)

* Thu Dec 17 2015 John Dulaney <jdulaney@fedoraproject.org> - 1.4.1-1
- Update to latest upstream release

* Fri Dec 11 2015 John Dulaney <jdulaney@fedoraproject.org> - 1.3.1-1
- Update to latest upstream release

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 1.1.2-4
- Rebuilt for Python3.5 rebuild

* Wed Jul 15 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.1.2-3
- Modernize spec file
- add missing source

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 16 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.1.2-2
- Update to 1.1.2
- Fix license

* Tue Aug 19 2014 Eric Smith <spacewar@gmail.com> 0.8.6-1
- Update to latest upstream.
- No python3 in el7.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Feb 26 2014 Eric Smith <spacewar@gmail.com> 0.8.1-1
- Update to latest upstream.

* Tue Aug 13 2013 Eric Smith <spacewar@gmail.com> 0.6-5
- Add Requires of python{,3}-pycparser.

* Thu Jul 25 2013 Eric Smith <spacewar@gmail.com> 0.6-4
- Fix broken conditionals in spec (missing question marks), needed for el6.

* Tue Jul 23 2013 Eric Smith <spacewar@gmail.com> 0.6-3
- Add Python3 support.

* Mon Jul 22 2013 Eric Smith <spacewar@gmail.com> 0.6-2
- Better URL, and use version macro in Source0.

* Sun Jul 21 2013 Eric Smith <spacewar@gmail.com> 0.6-1
- initial version
