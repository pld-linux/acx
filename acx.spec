#
#
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Name:		kernel-net-acx100
Version:	0.2.0pre7_plus_fixes_3
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://rhlx01.fht-esslingen.de/~andi/acx100/acx100-%{version}.tar.bz2
# Source0-md5:	31533c147e4f1f268ee41a3c531ba6ab
URL:		http://acx100.sourcefroge.net/index.html
%{?with_dist_kernel:BuildRequires:	kernel-headers >= 2.4.0}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
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
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-acx100
Linux SMP driver for WLAN card base on ACX100.

%description -n kernel-smp-net-acx100 -l pl
Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100.

%prep
%setup -q -n acx100-%{version}

%build
cd src
ln -sf %{_kernelsrcdir}/config-up .config
rm -rf include
install -d include/{linux,config}
cp ../include/* include/
ln -s %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -s %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
echo 'acx100_pci-objs := acx100.o acx100_conv.o acx100_helper.o acx100_helper2.o acx100_ioctl.o acx80211frm.o idma.o ihw.o' > Makefile
echo 'obj-m = acx100_pci.o'>>Makefile
echo 'obj-m = acx100_usb.o'>>Makefile
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules

mv acx100_pci.ko acx100_pci.ko-done
mv acx100_usb.ko acx100_usb.ko-done

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper

ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
cp ../include/* include/
ln -s %{_kernelsrcdir}/include/linux/autoconf-smp.h include/linux/autoconf.h
ln -s %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
echo 'acx100_pci-objs := acx100.o acx100_conv.o acx100_helper.o acx100_helper2.o acx100_ioctl.o acx80211frm.o idma.o ihw.o' > Makefile
echo 'obj-m = acx100_pci.o'>>Makefile
echo 'obj-m = acx100_usb.o'>>Makefile
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install src/acx100_pci.ko-done $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/acx100_pci.ko
install src/acx100_usb.ko-done $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/acx100_usb.ko
install src/acx100_pci.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/acx100_pci.ko
install src/acx100_usb.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/acx100_usb.ko

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
