Name: kernel-devel
Summary: The Linux Kernel development files
Version: 5.11.0
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source: %{name}-%{version}.tar.gz
Provides: %{name}-%{version}
%define __spec_install_post /usr/lib/rpm/brp-compress || :

%description
This package provides makefiles sufficient to build modules against the kernel package.

%prep
%setup -q

%build
echo "nothing to do ..."

%install
mkdir -p %{buildroot}/usr/src/kernels/%{version}
find . -iname "Makefile*" -o -iname "Kconfig*" -o -iname ".config" -o -iname "Module.symvers" -o -iname "System.map" -o -iname "vmlinux.id" > /tmp/filelist.txt
cp -r --parent $(cat /tmp/filelist.txt) %{buildroot}/usr/src/kernels/%{version}

%clean
rm -rf /tmp/filelist.txt

%files
%defattr (-, root, root)
/usr/src/kernels/%{version}
