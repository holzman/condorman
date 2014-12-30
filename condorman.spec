%define prefix_frontend /var/lib/djangoapp
%define prefix_backend /var/lib/condorman-backend

Name:		condorman
Version:        1.0
Release:        0%{?dist}
Summary:        HTCondor Batch Priority Manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         condorman-%{version}.tar.gz
AutoReqProv: no
BuildArch:   noarch
Group: default
License:        Fermitools Software Legal Information (Modified BSD License)
Packager: 	Burt Holzman <burt@fnal.gov>
%description
HTCondor Batch Priority Manager



%package frontend
Summary: HTCondor Batch Priority Manager frontend
Prefix: 	%{prefix_frontend}
%description frontend
This package manages batch priority for HTCondor systems via a django app, web frontend, and postgres db.

%package backend
Summary: HTCondor Batch Priority Manager backend
Prefix: 	%{prefix_backend}
%description backend
A simple python script to query the postgres db and adjust HTCondor priorities. This should be installed on the HTCondor central manager.

%prep
%setup -n condorman-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{prefix_frontend}

cp -av condorman %{buildroot}/%{prefix_frontend}
cp -a mysite %{buildroot}/%{prefix_frontend}
cp -a templates %{buildroot}/%{prefix_frontend}
cp -a manage.py %{buildroot}/%{prefix_frontend}

mkdir -p %{buildroot}/%{prefix_backend}
cp -av backend/* %{buildroot}/%{prefix_backend}

%clean

%files backend
%defattr(-,root,root,-)
%{prefix_backend}

%files frontend
%defattr(-,root,root,-)
%{prefix_frontend}/condorman
%{prefix_frontend}/mysite
%{prefix_frontend}/manage.py
%{prefix_frontend}/manage.py[c|o]
%{prefix_frontend}/templates

%changelog

