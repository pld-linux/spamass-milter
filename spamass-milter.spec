Summary:	Spamassassin Milter
Name:		spamass-milter
Version:	0.3.0
Release:	0.1
License:	GPL
Group:		System Environment/Daemons
Source0:	http://savannah.nongnu.org/download/spamass-milt/%{name}-%{version}.tar.gz
# Source0-md5:	ced600331a0df7609fdbdf0e6d0eb943
Source1:        %{name}.init
URL:		http://savannah.gnu.org/projects/spamass-milt/
BuildRequires:	libstdc++-devel
BuildRequires:	sendmail-devel
BuildRequires:	spamassassin
BuildRequires:	spamassassin-spamc
Requires:	spamassassin
# Requires sendmail to have milter support, too.
Requires:	sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A little plugin for the Sendmail Milter (Mail Filter) library that pipes all
incoming mail (including things received by rmail/UUCP) through the
SpamAssassin, a highly customizable SpamFilter.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/spamass-milter

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add spamass-milter

if [ -f /var/lock/subsys/spamass-milter ]; then
    /etc/rc.d/init.d/spamass-milter restart >&2
else
    echo "Run \"/etc/rc.d/init.d/spamass-milter start\" to start spamass-milter daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/spamass-milter ]; then
            /etc/rc.d/init.d/spamass-milter stop >&2
        fi
    /sbin/chkconfig --del spamass-milter
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_sbindir}/spamass-milter
%attr(754,root,root) /etc/rc.d/init.d/spamass-milter
%{_initrddir}/spamass-milter
%{_mandir}/man1/spamass-milter.1*
