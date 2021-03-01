Name: kernel
Summary: The Linux Kernel
Version: 5.11.0
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source: %{name}-%{version}.tar.gz
Provides: %{name}-%{version}
%define __spec_install_post /usr/lib/rpm/brp-compress || :

Requires: kernel-devel-%{version}
Requires: kernel-headers-%{version}
Requires: kernel-modules-%{version}


%description
The Linux Kernel, the operating system core itself

%prep
%setup -q

%build
make -j2 KBUILD_BUILD_VERSION=%{release} bzImage

%install
mkdir -p %{buildroot}/boot
cp $( image_name) %{buildroot}/boot/vmlinuz-
cp System.map %{buildroot}/boot/System.map-
cp .config %{buildroot}/boot/config-

%post
if [ -x /sbin/installkernel -a -r /boot/vmlinuz- -a -r /boot/System.map- ]; then
cp /boot/vmlinuz- /boot/.vmlinuz--rpm
cp /boot/System.map- /boot/.System.map--rpm
rm -f /boot/vmlinuz- /boot/System.map-
/sbin/installkernel  /boot/.vmlinuz--rpm /boot/.System.map--rpm
rm -f /boot/.vmlinuz--rpm /boot/.System.map--rpm
fi

%preun
if [ -x /sbin/new-kernel-pkg ]; then
new-kernel-pkg --remove  --rminitrd --initrdfile=/boot/initramfs-.img
elif [ -x /usr/bin/kernel-install ]; then
kernel-install remove 
fi

%postun
if [ -x /sbin/update-bootloader ]; then
/sbin/update-bootloader --remove 
fi

%files
%defattr (-, root, root)
/boot/*
