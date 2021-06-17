Name: linux
Summary: The Linux Kernel
Version: 5.12.10
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: %{name}-%{version}.tar.gz
Source1: fedora-x86_64.config
Patch0: 0001-MultiQueue-Skiplist-Scheduler-v0.210.patch
Provides: %{name}-%{version}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%description
The Linux Kernel, the operating system core itself

%package -n headers
Summary: Header files for the Linux kernel
Group: Development/System

%description -n headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package -n modules
Summary: modules files for the Linux kernel
Group: Development/System
%description -n modules
This package provides commonly used kernel modules for the core kernel package.

%package -n devel
Summary: Development package for building kernel modules to match the %{version} kernel
Group: System Environment/Kernel
%description -n devel
This package provides kernel headers and makefiles sufficient to build modules
against the %{version} kernel package.


%setup -q
%patch0 -p1
cp -r %{Source1} .config

%build
 yes "" | make oldconfig
make -j8 KBUILD_BUILD_VERSION=%{release}

%install
# For kernel
mkdir -p %{buildroot}/boot
cp $(make image_name) %{buildroot}/boot/vmlinuz-%{version}
cp System.map %{buildroot}/boot/System.map-%{version}
cp .config %{buildroot}/boot/config-%{version}

# For kernel-modules
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot}/modules_tmp modules_install
cd %{buildroot}/modules_tmp/lib/modules/%{version}
rm -f %{buildroot}/lib/modules/%{version}/build
rm -f %{buildroot}/lib/modules/%{version}/source
ln -sf /usr/src/kernels/%{version} build
ln -sf /usr/src/kernels/%{version} source
mkdir -p %{buildroot}/lib/modules/%{version}
cp -rp $(cat ../../modules.list) %{buildroot}/lib/modules/%{version}

# For kernel-headers
make %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

# For kernel-devel
mkdir -p %{buildroot}/usr/src/kernels/%{version}
cp -r --parent $(find . -iname "Makefile*" -o -iname "Kconfig*" -o -iname ".config" -o -iname "Module.symvers" -o -iname "System.map" -o -iname "vmlinux.id") %{buildroot}/usr/src/kernels/%{version}

%clean
rm -rf %{buildroot}

%post
if [ -x /sbin/installkernel -a -r /boot/vmlinuz-%{version} -a -r /boot/System.map-%{version} ]; then
cp /boot/vmlinuz-%{version} /boot/.vmlinuz-%{version}-rpm
cp /boot/System.map-%{version} /boot/.System.map-%{version}-rpm
rm -f /boot/vmlinuz-%{version} /boot/System.map-%{version}
/sbin/installkernel %{version} /boot/.vmlinuz-%{version}-rpm /boot/.System.map-%{version}-rpm
rm -f /boot/.vmlinuz-%{version}-rpm /boot/.System.map-%{version}-rpm
fi

%preun
if [ -x /sbin/new-kernel-pkg ]; then
new-kernel-pkg --remove %{version} --rminitrd --initrdfile=/boot/initramfs-%{version}.img
elif [ -x /usr/bin/kernel-install ]; then
kernel-install remove %{version}
fi

%postun
if [ -x /sbin/update-bootloader ]; then
/sbin/update-bootloader --remove %{version}
fi

%files
%defattr (-, root, root)
/boot/*

%files -n modules
%defattr (-, root, root)
/lib/modules/%{version}

%files -n headers
%defattr (-, root, root)
/usr/include

%files -n devel
%defattr (-, root, root)
/usr/src/kernels/%{version}
