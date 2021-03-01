Name: kernel-headers
Summary: The Linux Kernel header files
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
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%prep
%setup -q

%build
echo "nothing to do ..."

%install
make -j2 INSTALL_HDR_PATH=%{buildroot}/usr headers_install

%files
%defattr (-, root, root)
/usr/include
