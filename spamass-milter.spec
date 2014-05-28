Summary:	Spamassassin Milter
Summary(pl.UTF-8):	Milter dla Spamassassina
Name:		spamass-milter
Version:	0.3.2
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://savannah.nongnu.org/download/spamass-milt/%{name}-%{version}.tar.gz
# Source0-md5:	964b011fe7d7eddfdb6d94f4767feab8
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-syntax.patch
Patch1:		%{name}-authuser.patch
Patch2:		%{name}-rcvd.patch
Patch3:		%{name}-bits.patch
Patch4:		%{name}-group.patch
Patch5:		%{name}-ipv6.patch
Patch6:		%{name}-rejectmsg.patch
URL:		https://savannah.nongnu.org/projects/spamass-milt/
BuildRequires:	libmilter-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	spamassassin
BuildRequires:	spamassassin-spamc
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	spamassassin
# Requires sendmail to have milter support, too.
Requires:	postfix
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A little plugin for the Sendmail Milter (Mail Filter) library that
pipes all incoming mail (including things received by rmail/UUCP)
through the SpamAssassin, a highly customizable SpamFilter.

%description -l pl.UTF-8
Mała wtyczka dla biblioteki Sendmail Milter (Mail Filter)
przepuszczająca całą przychodzącą pocztę (włącznie z rzeczami
otrzymanymi przez rmaila/UUCP) przez SpamAssasina - wysoko
konfigurowalny filtr antyspamowy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0

%build
%configure \
	SENDMAIL=/usr/lib/sendmail
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/spamass-milter
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/spamass-milter

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add spamass-milter
%service spamass-milter restart

%preun
if [ "$1" = "0" ]; then
	%service spamass-milter stop
	/sbin/chkconfig --del spamass-milter
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_sbindir}/spamass-milter
%attr(754,root,root) /etc/rc.d/init.d/spamass-milter
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/spamass-milter
%{_mandir}/man1/spamass-milter.1*
