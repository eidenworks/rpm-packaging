Name:           flink
Version:        1.3.0
Release:        1%{?dist}
Summary:        Apache Flink

License:        ASL 2.0
URL:            http://flink.apache.com
Source0:        http://ftp.wayne.edu/apache/flink/flink-1.3.0/flink-1.3.0-bin-hadoop27-scala_2.10.tgz
Source1:        flink.service

BuildRequires:  tar
Requires:       java, redhat-lsb

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global __jar_repack %{nil}

%description
Apache Flink is an open-source stream processing framework for distributed, high-performing, always-available, and accurate data streaming applications.

%prep
%setup -q -n flink-1.2.1
cp -av %{SOURCE1} .

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT/opt/flink

#Create content dirs
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/flink

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 flink.service $RPM_BUILD_ROOT%{_unitdir}/

cp -parf * $RPM_BUILD_ROOT/opt/flink

%pre
# Add the "flink" user
getent group flink >/dev/null || groupadd -g 372 -r flink
getent passwd flink >/dev/null || \
  useradd -r -u 372 -g flink -s /bin/sh \
    -d /opt/flink -c "Apache Flink" flink
exit 0

%post
%systemd_post flink.service

%preun
%systemd_preun flink.service

%postun
%systemd_postun

%files
%defattr(-,flink,flink,755)
%license LICENSE
%doc README.txt

%dir %attr(755,flink,flink) %{_var}/lib/flink

%attr(644,root,root) %{_unitdir}/flink.service

/opt/flink

%changelog
* Mon May 29 2017 Miguel Perez Colino <mperez@redhat.com> release 1
- Initial RPM
