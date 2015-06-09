#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Math
%define		pnam	NumSeq
%include	/usr/lib/rpm/macros.perl
Summary:	Math::NumSeq -- number sequences
Name:		perl-Math-NumSeq
Version:	71
Release:	1
License:	GPL
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Math/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	c3d6104e4ce98cbb2b46239ed258c2cf
URL:		http://search.cpan.org/dist/Math-NumSeq/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Math::Factor::XS) >= 0.40
BuildRequires:	perl(Math::Prime::XS) >= 0.23
BuildRequires:	perl-constant-defer >= 1
BuildRequires:	perl-File-HomeDir
BuildRequires:	perl-Math-Libm
BuildRequires:	perl-Module-Util
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a base class for some number sequences.  Sequence objects can
iterate through values and some sequences have random access and/or a
predicate test.

The idea is to generate things like squares or primes in a generic way.
Some sequences, like squares, are so easy there's no need for a class except
for the genericness.  Other sequences are trickier and an iterator is a good
way to go through values.  The iterating tries to be progressive, so not
calculating too far ahead yet doing reasonable size chunks for efficiency.

Sequence values have an integer index "i" starting either from i=0 or i=1 or
whatever best suits the sequence.  The values can be anything, positive,
negative, fractional, etc.

The intention is that all modules Math::NumSeq::Foo are sequence classes,
and that supporting things are deeper, such as under
Math::NumSeq::Something::Helper or Math::NumSeq::Base::SharedStuff.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorlib}/Math/NumSeq
%{perl_vendorlib}/Math/NumSeq.pm
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
