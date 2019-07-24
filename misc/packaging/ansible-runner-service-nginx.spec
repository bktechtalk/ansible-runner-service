%if 0%{?rhel} == 7
  # Building on CentoOS 7 would result in ".el7.centos"
  %define dist .el7
%endif

Name: ansible-runner-service
Version: 0.94
Release: 3%{?dist}
Summary: RESTful API for ansible/ansible_runner execution
Source0: https://github.com/ansible/%{name}/archive/%{name}-%{version}.tar.gz
Group:	 Applications/System
License: ASL 2.0

BuildArch: noarch

BuildRequires: python-setuptools
BuildRequires: python-devel

Requires: gcc
Requires: ansible >= 2.6
Requires: ansible-runner >= 1.3.2
Requires: python-flask >= 1.0.2
Requires: python2-flask-restful >= 0.3.5
Requires: python2-cryptography
Requires: openssl
Requires: pyOpenSSL
Requires: PyYAML
Requires: nginx
Requires: uwsgi

%description
This package provides a daemon that exposes a REST API interface on top of the functionality provided by ansible and ansible_runner.

The daemon (ansible-runner-service) listens on https://localhost:5001 by default for playbook or ansible inventory requests. For developers interested in using the API, all the available endpoints are documented at https://localhost:5001/api.

In addition to the API endpoints, the daemon also provides a /metrics endpoint for prometheus integration. A sample Grafana dashboard is provided within /usr/share/doc/ansible-runner-service

%prep
%setup -q -n %{name}-%{version}

%build
# Disable debuginfo packages
%define _enable_debug_package 0
%define debug_package %{nil}

%{__python} setup.py build

%install
# Installation
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-scripts /usr/bin

# Configuration and log files
mkdir -p %{buildroot}%{_sysconfdir}/ansible-runner-service
install -m 0644 ./config.yaml %{buildroot}%{_sysconfdir}/ansible-runner-service
install -m 0644 ./logging.yaml %{buildroot}%{_sysconfdir}/ansible-runner-service

# Prepare support folders
mkdir -p %{buildroot}%{_prefix}/share/ansible-runner-service/artifacts
mkdir -p %{buildroot}%{_prefix}/share/ansible-runner-service/env
mkdir -p %{buildroot}%{_prefix}/share/ansible-runner-service/inventory
mkdir -p %{buildroot}%{_prefix}/share/ansible-runner-service/project
mkdir -p %{buildroot}%{_prefix}/share/ansible-runner-service/client_cert

# Copy example playbooks
install -m 0644 ./samples/project/runnertest.yml %{buildroot}%{_prefix}/share/ansible-runner-service/project

# Prepare metrics dashboard
mkdir -p %{buildroot}%{_docdir}/ansible-runner-service/dashboards
install -m 0644 ./misc/dashboards/ansible-runner-service-metrics.json  %{buildroot}%{_docdir}/ansible-runner-service/dashboards

# Copy license
install -m 0644 ./LICENSE.md %{buildroot}%{_docdir}/ansible-runner-service

# Copy wsgi file
mkdir -p %{buildroot}%{_sysconfdir}/nginx/conf.d
install -m 0644 ./misc/nginx/ars_site_nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d
install -m 0644 ./misc/nginx/uwsgi.ini %{buildroot}%{_sysconfdir}/ansible-runner-service

%post
# Copy Ansible Runner Service Site config file for Nginx
/bin/systemctl --system daemon-reload &> /dev/null || :

%postun
/bin/systemctl --system daemon-reload &> /dev/null || :

%files
%{_bindir}/ansible_runner_service
%{python_sitelib}/*
%{_prefix}/share/ansible-runner-service/*
%{_sysconfdir}/ansible-runner-service/*
%{_sysconfdir}/nginx/conf.d/*
%{_docdir}/ansible-runner-service/*


%changelog
* Fri Mar 29 2019 Juan Migul Olmo <jolmomar@redhat.com> 0.9-4
- Provide functionality using Nginx service with TLS mutual authentication
* Sun Feb 10 2019 Paul Cuzner <pcuzner@redhat.com> 0.9-3
- minor updates to improve packaging workflow
* Mon Dec 17 2018 Paul Cuzner <pcuzner@redhat.com> 0.9
- Repackaged for 0.9, including more specific package dependencies
* Mon Sep 24 2018 Paul Cuzner <pcuzner@redhat.com> 0.8
- initial rpm packaging
