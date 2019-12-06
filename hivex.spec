# Conditionalize Ocaml support.  This looks ass-backwards, but it's not.
%ifarch %{ocaml_native_compiler}
%bcond_without ocaml
%else
%bcond_with ocaml
%endif

# Verify tarball signature with GPGv2.
%global verify_tarball_signature 1

Name:           hivex
Version:        1.3.15
Release:        1
Summary:        Read and write Windows Registry binary hive files

License:        LGPLv2
URL:            http://libguestfs.org/

Source0:        %{name}-%{version}.tar.gz
%if 0%{verify_tarball_signature}
Source1:        %{name}-%{version}.tar.gz.sig
%endif

# Keyring used to verify tarball signature.
%if 0%{verify_tarball_signature}
Source2:       libguestfs.keyring
%endif

# Upstream patch to fix injection of LDFLAGS.
# https://bugzilla.redhat.com/show_bug.cgi?id=1548536
Patch1:         0001-ocaml-Link-the-C-bindings-with-LDFLAGS-RHBZ-1548536.patch
BuildRequires:  autoconf, automake, libtool, gettext-devel

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
BuildRequires:  python2-devel, python-unversioned-command
BuildRequires:  python3-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  rubygem(json)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rdoc)
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel
%if 0%{verify_tarball_signature}
BuildRequires: gnupg2
%endif

Provides:      bundled(gnulib)


%description
Hive files are the undocumented binary files that Windows uses to
store the Windows Registry on disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexregedit' (in perl-hivex) lets you export and merge to the
textual regedit format.

'hivexml' can be used to convert a hive file to a more useful XML
format.

In order to get access to the hive files themselves, you can copy them
from a Windows machine.  They are usually found in
%%systemroot%%\system32\config.  For virtual machines we recommend
using libguestfs or guestfish to copy out these files.  libguestfs
also provides a useful high-level tool called 'virt-win-reg' (based on
hivex technology) which can be used to query specific registry keys in
an existing Windows VM.

For OCaml bindings, see 'ocaml-hivex-devel'.

For Perl bindings, see 'perl-hivex'.

For Python 2 bindings, see 'python2-hivex'.

For Python 3 bindings, see 'python3-hivex'.

For Ruby bindings, see 'ruby-hivex'.


%package devel
Summary:        Development tools and libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package static
Summary:        Statically linked library for %{name}
Requires:       %{name} = %{version}-%{release}


%description static
%{name}-static contains the statically linked library
for %{name}.


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


%package -n python2-%{name}
Summary:       Python 2 bindings for %{name}
Requires:      %{name} = %{version}-%{release}

# Can be removed in Fedora 29.
Obsoletes:     python-%{name} < %{version}-%{release}
Provides:      python-%{name} = %{version}-%{release}

%description -n python2-%{name}
python2-%{name} contains Python 2 bindings for %{name}.


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
%if 0%{verify_tarball_signature}
tmphome="$(mktemp -d)"
gpgv2 --homedir "$tmphome" --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%endif
%setup -q
%autopatch -p1

# Because the patch touches Makefile.am, rerun autotools.
autoreconf -i -f

# Build Python 3 bindings in a separate subdirectory.  We have to
# build everything twice unfortunately.
copy="$(mktemp -d)"
cp -a . "$copy"
mv "$copy" python3


%build
%configure \
%if !%{with ocaml}
    --disable-ocaml \
%endif
    %{nil}
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}

pushd python3
%configure \
    PYTHON=/usr/bin/python3 \
    --disable-ocaml --disable-perl --disable-ruby
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}
popd


%install
# Install Python3 first so the "real" install below overwrites
# everything else.
pushd python3
make install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor
popd
make install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

# Remove unwanted Python files:
rm $RPM_BUILD_ROOT%{python2_sitearch}/libhivexmod.la
rm $RPM_BUILD_ROOT%{python3_sitearch}/libhivexmod.la

%find_lang %{name}


%check
make check

pushd python3
make check
popd


%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


%files static
%doc LICENSE
%{_libdir}/libhivex.a


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
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*
%{_bindir}/hivexregedit
%{_mandir}/man1/hivexregedit.1*


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
* Sat Nov 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.3.15-1
- Package init
