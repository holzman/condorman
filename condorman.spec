Name:		condorman
Version:        1.0
Release:        0%{?dist}
Summary:        HTCondor Batch Priority Manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix: 	/var/lib/djangoapp
Source:         condorman-%{version}.tar.gz
AutoReqProv: no
BuildArch:   noarch

Group: default
License:        Fermitools Software Legal Information (Modified BSD License)
Packager: 	Burt Holzman <burt@fnal.gov>

%description
Manages batch priority for HTCondor systems

%prep
%setup -n condorman-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{prefix}
#cd condorman-%{version}
cp -av condorman %{buildroot}/%{prefix}
cp -a mysite %{buildroot}/%{prefix}
cp -a templates %{buildroot}/%{prefix}
cp -a manage.py %{buildroot}/%{prefix}

%clean

%files
%defattr(-,root,root,-)

# Reject config files already listed or parent directories, then prefix files
# with "/", then make sure paths with spaces are quoted. I hate rpm so much.
%{prefix}/condorman
%{prefix}/mysite
%{prefix}/manage.py
%{prefix}/templates

%changelog

