#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
#
# TODO:
# - add firmware download?
#
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Name:		acx100
Version:	0.2.0pre8_plus_fixes_57
%define	_rel	1
Release:	%{_rel}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://rhlx01.fht-esslingen.de/~andi/acx100/%{name}-%{version}.tar.bz2
# Source0-md5:	f48eb1113764f150666644baf52656af
URL:		http://acx100.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.3}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ACX100 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%package -n kernel-net-acx100
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-acx100
This is driver for WLAN card based on ACX100 for Linux.

%description -n kernel-net-acx100 -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%package -n kernel-smp-net-acx100
Summary:	Linux SMP driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-acx100
Linux SMP driver for WLAN card base on ACX100.

%description -n kernel-smp-net-acx100 -l pl
Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100.

%prep
%setup -q

%define buildconfigs %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}

%build
mv src/Makefile2.6 src/Makefile
for cfg in %{buildconfigs}; do
	mkdir -p modules/$cfg
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -f include/asm
	chmod 000 modules
	install -d include/{linux,config}
	%{__make} -C %{_kernelsrcdir} clean \
		SUBDIRS=$PWD/src \
		O=$PWD \
		%{?with_verbose:V=1}
	install -d include/config
	chmod 700 modules
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-${cfg}.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm #FIXME
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} modules \
		SUBDIRS=$PWD/src \
		O=$PWD \
		%{?with_verbose:V=1}
	mv src/*.ko modules/$cfg/
done

%install
rm -rf $RPM_BUILD_ROOT

#Add directory to store firmware
install -d $RPM_BUILD_ROOT%{_datadir}/acx

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

for cfg in %{buildconfigs}; do
	cfgdest=''
	if [ "$cfg" = "smp" ]; then
		install modules/$cfg/*.ko \
			$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}$cfg/misc
	else
		install modules/$cfg/*.ko \
			$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-acx100
%depmod %{_kernel_ver}

%postun	-n kernel-net-acx100
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-acx100
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-acx100
%depmod %{_kernel_ver}smp

%files -n kernel-net-acx100
%defattr(644,root,root,755)
%doc ChangeLog README TODO doc/*
%dir %{_datadir}/acx
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp}
%files -n kernel-smp-net-acx100
%defattr(644,root,root,755)
%doc ChangeLog README TODO doc/*
%dir %{_datadir}/acx
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
