Name: report-engine
Version: %VERSION%
Release: 0
License: MIT
Requires: openssl, unzip
Prefix: /opt
Summary: fastapi report engine for liman backend services
Group: Applications/System
BuildArch: x86_64

%description
fastapi report engine for liman backend services

%pre

%prep

%build

%install
cp -rfa %{_app_dir} %{buildroot}

%post -p /bin/bash

if ! [ -f "/opt/report-engine/keys/report-engine.key" ]; then
    mkdir -p '/opt/report-engine/keys/'
    openssl req -x509 -newkey rsa:4096 -subj "/CN=$(hostname -I | cut -d" " -f1 | xargs)" -extensions SAN -reqexts SAN -config <(cat $(echo "$(openssl version -d | sed 's/.*"\(.*\)"/\1/g')/openssl.cnf") <(printf "\n[SAN]\nsubjectAltName=IP:$(hostname -I | cut -d" " -f1 | xargs),IP:127.0.0.1,DNS:$(hostname)")) -keyout /opt/report-engine/keys/report-engine.key -nodes -out /opt/report-engine/keys/report-engine.pem -sha256 -days 358000
fi

chmod -R 770 /opt/report-engine
chown -R root:root /opt/report-engine

if [ -f "/usr/lib/systemd/system/report-engine.service" ]; then
    rm -rf /usr/lib/systemd/system/report-engine.service
    systemctl disable report-engine.service
    systemctl stop report-engine.service
    systemctl daemon-reload report-engine.service
fi

echo """
[Unit]
Description=FastAPI Report Engine
[Service]
Type=simple
WorkingDirectory=/opt/report-engine
ExecStart=/opt/report-engine/report-engine
Restart=always
RestartSec=10
SyslogIdentifier=report-engine
KillSignal=SIGINT
User=root
Group=root
[Install]
WantedBy=multi-user.target
    """ > /etc/systemd/system/report-engine.service

systemctl daemon-reload
systemctl enable report-engine.service
systemctl restart report-engine.service

%clean

%files
%defattr(0770, root, root)
/opt/report-engine/*

%define _unpackaged_files_terminate_build 0