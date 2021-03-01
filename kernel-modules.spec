Name: kernel-modules
Summary: The Linux Kernel module files
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
The package provides kernel modules built for this kernel version

%prep
%setup -q

%build
make KBUILD_BUILD_VERSION=%{release} modules

%install
make -j2 INSTALL_MOD_PATH=%{buildroot} modules_install
rm -f %{buildroot}/lib/modules//build
rm -f %{buildroot}/lib/modules//source

cd %{buildroot}
ln -sf /usr/src/kernels/%{version} build
ln -sf build source

%files
%defattr (-, root, root)
/lib/modules//
