# TODO:
# - add firmware download?
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
#
%ifarch sparc
%undefine	with_smp
%endif
#
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Name:		acx
Version:	20060215
%define	_rel	1
Release:	%{_rel}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://195.66.192.167/linux/acx_patches/%{name}-%{version}.tar.bz2
# Source0-md5:	95bcd5df2365dfcfc78169b0331f69a2
URL:		http://acx100.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.3}
BuildRequires:	rpmbuild(macros) >= 1.286
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
#setup -q -n %{name}-%{version}
cd $RPM_BUILD_DIR
install -d %{name}-%{version}
cd %{name}-%{version}
tar xfj %{SOURCE0}
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%define buildconfigs %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}

%build
# kernel module(s)
cd %{name}-%{version}
#cd src
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
        if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
                exit 1
        fi
        install -d o/include/linux
        ln -sf %{_kernelsrcdir}/config-$cfg o/.config
        ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
        ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
        %{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
        install -d o/include/config
        touch o/include/config/MARKER
        ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#       patching/creating makefile(s) (optional)
#
        %{__make} -C %{_kernelsrcdir} clean \
                RCS_FIND_IGNORE="-name '*.ko' -o" \
                SYSSRC=%{_kernelsrcdir} \
                SYSOUT=$PWD/o \
                M=$PWD O=$PWD/o \
                %{?with_verbose:V=1}
        %{__make} -C %{_kernelsrcdir} modules \
                CC="%{__cc}" CPP="%{__cpp}" \
                SYSSRC=%{_kernelsrcdir} \
                SYSOUT=$PWD/o \
                M=$PWD O=$PWD/o \
                %{?with_verbose:V=1}

        mv acx{,-$cfg}.ko
done

%install
cd %{name}-%{version}
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
