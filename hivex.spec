%ifarch %{ocaml_native_compiler}
%bcond_without ocaml
%else
%bcond_with ocaml
%endif

Name:           hivex
Version:        1.3.17
Release:        2
Summary:        Windows Registry "hive" extraction library
License:        LGPLv2
URL:            http://libguestfs.org/

Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
Source1:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz.sig
Source2:        libguestfs.keyring

BuildRequires:  perl-interpreter, perl, perl-podlators, perl-devel, perl-generators, perl(bytes), perl(Carp), perl(Encode), perl(ExtUtils::MakeMaker), perl(Exporter), perl(IO::Scalar), perl(IO::Stringy), perl(strict), perl(Test::More), perl(utf8), perl(vars), perl(warnings), perl(XSLoader), perl(Test::Pod) >= 1.00, perl(Test::Pod::Coverage) >= 1.00

%if %{with ocaml}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
%endif

BuildRequires:  python2-devel, python-unversioned-command, python3-devel, ruby-devel, rubygem-rake, rubygem(json), rubygem(minitest), rubygem(rdoc), readline-devel, libxml2-devel, gnupg2

Provides:      bundled(gnulib)


%description
Hivex is a library for extracting the contents of Windows Registry "hive" files.  It is designed to be secure against buggy or
malicious registry files.

Unlike other tools in this area, it doesn't use the textual .REG format, because parsing that is as much trouble as parsing the
original binary format.  Instead it makes the file available through a C API, and then wraps this API in higher level scripting and GUI
tools.

There is a separate program to export the hive as XML (see hivexml(1)), or to navigate the file (see hivexsh(1)).  There is also a Perl
script to export and merge the file as a textual .REG (regedit) file, see hivexregedit(1).

If you just want to export or modify the Registry of a Windows virtual machine, you should look at virt-win-reg(1).

Hivex is also comes with language bindings for OCaml, Perl, Python and Ruby.


%package devel
Summary:        Development package for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

Provides:       %{name}-devel
Obsoletes:      %{name}-devel

%description devel
Development tools and libraries for %{name} are included in %{name}-devel.


%package_help


%if %{with ocaml}
%package -n ocaml-%{name}
Summary:       Provide OCaml bindings for %{name}
Requires:      %{name} = %{version}-%{release}

%description -n ocaml-%{name}
OCaml bindings for %{name} are included in ocaml-%{name}.

Only for toplevel and scripting access. To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel package.


%package -n ocaml-%{name}-devel
Summary:       Development package for %{name} OCaml bindings
Requires:      ocaml-%{name} = %{version}-%{release}
Requires:      %{name}-devel = %{version}-%{release}

%description -n ocaml-%{name}-devel
Development libraries required to use the OCaml bindings for %{name} are in ocaml-%{name}-devel.
%endif


%package -n perl-%{name}
Summary:       Provide perl bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-%{name}
Perl bindings for %{name} are included in perl-%{name}.


%package -n python2-%{name}
Summary:       Provide python 2 bindings for %{name}
Requires:      %{name} = %{version}-%{release}

Obsoletes:     python-%{name} < %{version}-%{release}
Provides:      python-%{name} = %{version}-%{release}

%description -n python2-%{name}
Python 2 bindings for %{name} are included in python2-%{name}.


%package -n python3-%{name}
Summary:       Provide python 3 bindings for %{name}
Requires:      %{name} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for %{name} are included in python3-%{name}.


%package -n ruby-%{name}
Summary:       Provide ruby bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(release)
Requires:      ruby
Provides:      ruby(hivex) = %{version}

%description -n ruby-%{name}
Ruby bindings for %{name} are included ruby-%{name}.


%prep
tmphome="$(mktemp -d)" && gpgv2 --homedir "$tmphome" --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1 -n %{name}-%{version}

copy="$(mktemp -d)" && cp -a . "$copy" && mv "$copy" python3


%build
%configure \
%if !%{with ocaml}
    --disable-ocaml \
%endif
    %{nil}
%make_build V=1 INSTALLDIRS=vendor

cd python3
%configure \
    PYTHON=/usr/bin/python3 \
    --disable-ocaml --disable-perl --disable-ruby
%make_build V=1 INSTALLDIRS=vendor
cd ..


%install
cd python3
%make_install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor
cd ..
%make_install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor

%find_lang %{name}


%check
make check

cd python3 && make check && cd ..


%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%exclude %{_libdir}/libhivex.la
%exclude %{_libdir}/perl5/perllocal.pod
%exclude %{python2_sitearch}/libhivexmod.la
%exclude %{python3_sitearch}/libhivexmod.la
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc
%{_libdir}/libhivex.a


%files help
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man3/hivex.3*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*


%if %{with ocaml}
%files -n ocaml-%{name}
%doc README
%{_libdir}/ocaml/hivex
%exclude %{_libdir}/ocaml/hivex/*.a
%exclude %{_libdir}/ocaml/hivex/*.cmxa
%exclude %{_libdir}/ocaml/hivex/*.cmx
%exclude %{_libdir}/ocaml/hivex/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%{_libdir}/ocaml/hivex/*.a
%{_libdir}/ocaml/hivex/*.cmxa
%{_libdir}/ocaml/hivex/*.cmx
%{_libdir}/ocaml/hivex/*.mli
%endif


%files -n perl-%{name}
%{perl_vendorarch}/*
%{_bindir}/hivexregedit


%files -n python2-%{name}
%{python2_sitearch}/hivex/
%{python2_sitearch}/*.so


%files -n python3-%{name}
%{python3_sitearch}/hivex/
%{python3_sitearch}/*.so


%files -n ruby-%{name}
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/hivex.rb
%{ruby_vendorarchdir}/_hivex.so


%changelog
* Sat Nov 30 2019 jiaxiya <jiaxiyajiaxiya@163.com> - 1.3.17-2
- Package init
