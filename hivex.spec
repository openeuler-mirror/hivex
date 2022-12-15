%ifarch %{ocaml_native_compiler}
%bcond_without ocaml
%else
%bcond_with ocaml
%endif

Name:           hivex
Version:        1.3.21
Release:        1
Summary:        Read and write Windows Registry binary hive files
License:        LGPLv2
URL:            http://libguestfs.org/
Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
Source1:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz.sig
Source2:        libguestfs.keyring

BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  %{_bindir}/pod2html
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(IO::Stringy)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
%if %{with ocaml}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
%endif
BuildRequires:  python3-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  rubygem(json)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rdoc)
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel
BuildRequires:  gnupg2
BuildRequires:  make

Provides:       bundled(gnulib)

%description
Hive files are the undocumented binary files that Windows uses to store the Windows Registry on disk.  
Hivex is a library that can read and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive binary file.

'hivexregedit' (in perl-hivex) lets you export and merge to the textual regedit format.

'hivexml' can be used to convert a hive file to a more useful XML format.

In order to get access to the hive files themselves, you can copy them from a Windows machine.  They are 
usually found in %%systemroot%%\system32\config.  For virtual machines we recommend using libguestfs or 
guestfish to copy out these files.  libguestfs also provides a useful high-level tool called 'virt-win-reg'
 (based on hivex technology) which can be used to query specific registry keys in an existing Windows VM.

For OCaml bindings, see 'ocaml-hivex-devel'.

For Perl bindings, see 'perl-hivex'.

For Python 3 bindings, see 'python3-hivex'.

For Ruby bindings, see 'ruby-hivex'.


%package devel
Summary:        Development tools and libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

Provides:       %{name}-static = %{version}-%{release}
Obsoletes:      %{name}-static < %{version}-%{release}

%description devel
%{name}-devel contains development tools and libraries for %{name}.


%package_help


%if %{with ocaml}
%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Requires:      %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Requires:      ocaml-%{name} = %{version}-%{release}
Requires:      %{name}-devel = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.
%endif


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python3-%{name}
Summary:       Python 3 bindings for %{name}
Requires:      %{name} = %{version}-%{release}

%description -n python3-%{name}
python3-%{name} contains Python 3 bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(release)
Requires:      ruby
Provides:      ruby(hivex) = %{version}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%prep
tmphome="$(mktemp -d)" && gpgv2 --homedir "$tmphome" --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -n %{name}-%{version}


%build
%configure \
    PYTHON=%{__python3} \
%if !%{with ocaml}
    --disable-ocaml \
%endif
    %{nil}
%make_build V=1 INSTALLDIRS=vendor


%install
%make_install INSTALLDIRS=vendor

%find_lang %{name}


%check
make check


%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%exclude %{_libdir}/libhivex.la
%exclude %{_libdir}/perl5/perllocal.pod
%exclude %{python3_sitearch}/libhivexmod.la


%files devel
%doc LICENSE
%{_libdir}/libhivex.so
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

%files -n python3-%{name}
%{python3_sitearch}/hivex/
%{python3_sitearch}/*.so


%files -n ruby-%{name}
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/hivex.rb
%{ruby_vendorarchdir}/_hivex.so


%changelog
* Wed Oct 12 2022 hantingxiang <hantingxiang@gmail.com> - 1.3.21-1
- update version to 1.3.21

* Fri Sep 24 2021 yaoxin <yaoxin30@huawei.com> - 1.3.17-5
- Fix CVE-2021-3622

* Tue May 25 2021 wangyue <wangyue92@huawei.com> - 1.3.17-4
- Fix CVE-2021-3504

* Wed Oct 21 2020 leiju <leiju4@163.com> - 1.3.17-3
- remove python2 subpackage

* Sat Nov 30 2019 jiaxiya <jiaxiyajiaxiya@163.com> - 1.3.17-2
- Package init
