Summary:	Spamassassin Milter
Summary(pl.UTF-8):	Milter dla Spamassassina
Name:		spamass-milter
Version:	0.4.0
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://savannah.nongnu.org/download/spamass-milt/%{name}-%{version}.tar.gz
# Source0-md5:	aae2624770f5cb5a8b6484afb0fe5baa
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-rcvd.patch
Patch1:		%{name}-group.patch
URL:		https://savannah.nongnu.org/projects/spamass-milt/
BuildRequires:	libmilter-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	spamassassin
BuildRequires:	spamassassin-spamc
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	spamassassin
Requires:	spamassassin-spamc
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
