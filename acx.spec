#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Name:		kernel-net-acx100
Version:	0.2.0pre8_plus_fixes_18
%define	_rel	2
Release:	%{_rel}@%{_kernel_ver_str}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://rhlx01.fht-esslingen.de/~andi/acx100/acx100-%{version}.tar.bz2
#Source0-MD5:   430aa98bc3cc3e7ee0cb0e0c170f4f8c
URL:		http://acx100.sourcefroge.net/index.html
%{?with_dist_kernel:BuildRequires:	kernel-headers >= 2.4.0}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-net-acx100
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ACX100 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%package -n kernel-smp-net-acx100
Summary:	Linux SMP driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-acx100
Linux SMP driver for WLAN card base on ACX100.

%description -n kernel-smp-net-acx100 -l pl
Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100.

%prep
%setup -q -n acx100-%{version}

%build
cat > config.mk <<EOF
KERNEL_BUILD=%{_kernelsrcdir}
VERSION_CODE=`grep LINUX_VERSION_CODE %{_kernelsrcdir}/include/linux/version.h | sed -e 's/[^0-9]//g'`
EOF
%{__make} \
	CC="%{kgcc}" \
	CPPFLAGS="-D__KERNEL__ -DMODULE -DACX_DEBUG=1 -DWLAN_HOSTIF=WLAN_PCI -I%{_kernelsrcdir}/include -I../include" \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing -fno-common -fomit-frame-pointer -Wall -Wstrict-prototypes -Wno-trigraphs -mpreferred-stack-boundary=4 -pipe -DACX_IO_WIDTH=32"

mv -f src/acx_pci.o acx_pci-up.o
mv -f src/acx_usb.o acx_usb-up.o

%{__make} clean -C src
%{__make} \
	CC="%{kgcc}" \
	CPPFLAGS="-D__KERNEL__ -D__KERNEL_SMP -DMODULE -DACX_DEBUG=1 -DWLAN_HOSTIF=WLAN_PCI -I%{_kernelsrcdir}/include -I../include" \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing -fno-common -fomit-frame-pointer -Wall -Wstrict-prototypes -Wno-trigraphs -mpreferred-stack-boundary=4 -pipe -DACX_IO_WIDTH=32"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install acx_pci-up.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/acx_pci.o
install acx_usb-up.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/acx_usb.o
install src/acx_pci.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/acx_pci.o
install src/acx_usb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/acx_usb.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-acx100
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-acx100
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO doc/*
/lib/modules/%{_kernel_ver}/misc/*.o*

%files -n kernel-smp-net-acx100
%defattr(644,root,root,755)
%doc ChangeLog README TODO doc/*
/lib/modules/%{_kernel_ver}smp/misc/*.o*
