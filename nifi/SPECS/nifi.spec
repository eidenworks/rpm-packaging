Name:           nifi
Version:        1.2.0
Release:        4%{?dist}
Summary:        Apache NiFi

License:        ASL 2.0
URL:            http://nifi.apache.com
Source0:        http://apache.rediris.es/nifi/1.2.0/nifi-1.2.0-bin.tar.gz
Source1:        nifi.service
Source2:        nifi.firewall
Source3:        nifi.properties

BuildRequires:  tar
Requires:       java, redhat-lsb

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global __jar_repack %{nil}

%description
Apache NiFi supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic. Some of the high-level capabilities and objectives of Apache NiFi include:

Web-based user interface
Seamless experience between design, control, feedback, and monitoring
Highly configurable
Loss tolerant vs guaranteed delivery
Low latency vs high throughput
Dynamic prioritization
Flow can be modified at runtime
Back pressure
Data Provenance
Track dataflow from beginning to end
Designed for extension
Build your own processors and more
Enables rapid development and effective testing
Secure SSL, SSH, HTTPS, encrypted content, etc...
Multi-tenant authorization and internal authorization/policy management

%prep
%setup -q -n nifi-1.2.0
cp -av %{SOURCE1} .
cp -av %{SOURCE2} .
mv conf/nifi.properties conf/nifi.properties_original
cp -av %{SOURCE3} ./conf/

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT/opt/nifi

#Create content dirs
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/nifi/data/database_repository
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/nifi/data/flowfile_repository
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/nifi/data/content_repository
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/nifi/data/provenance_repository


mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 nifi.service $RPM_BUILD_ROOT%{_unitdir}/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/firewalld/services/
install -p -m 644 -T nifi.firewall $RPM_BUILD_ROOT%{_sysconfdir}/firewalld/services/nifi.xml

cp -parf * $RPM_BUILD_ROOT/opt/nifi

%pre
# Add the "nifi" user
getent group nifi >/dev/null || groupadd -g 371 -r nifi
getent passwd nifi >/dev/null || \
  useradd -r -u 371 -g nifi -s /bin/sh \
    -d /opt/nifi -c "Apache NiFi" nifi
exit 0

%post
%systemd_post nifi.service


%preun
%systemd_preun nifi.service

%postun
%systemd_postun

%files
%defattr(-,nifi,nifi,755)
%license LICENSE
%doc README

%dir %attr(755,nifi,nifi) %{_var}/lib/nifi/data/database_repository
%dir %attr(755,nifi,nifi) %{_var}/lib/nifi/data/flowfile_repository
%dir %attr(755,nifi,nifi) %{_var}/lib/nifi/data/content_repository
%dir %attr(755,nifi,nifi) %{_var}/lib/nifi/data/provenance_repository

%attr(644,root,root) %{_unitdir}/nifi.service
%attr(644,root,root) %{_sysconfdir}/firewalld/services/nifi.xml

/opt/nifi

%changelog
* Mon May 29 2017 Miguel Perez Colino <mperez@redhat.com> release 4
- Added content dirs
- Improved firewalld rules (only ports 8080 and 8081 to be opened)
- Added different default properties

* Mon May 29 2017 Miguel Perez Colino <mperez@redhat.com> release 3
- Added initial firewalld file
- Enforced permissions on firewall and service files

* Mon May 29 2017 Miguel Perez Colino <mperez@redhat.com> release 2
- Added systemd service
- Corrected default permissions
- Added macros to target dirs

* Thu May 11 2017 Miguel Perez Colino <mperez@redhat.com> release 1
- Initial RPM
