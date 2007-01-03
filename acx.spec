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
Version:	20060521
%define	_rel	1
Release:	%{_rel}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://195.66.192.167/linux/acx_patches/%{name}-%{version}.tar.bz2
# Source0-md5:	d6a59fc3d34fd596fbd345c24d50a4eb
Patch0:		%{name}-include.patch
URL:		http://acx100.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.16}
BuildRequires:	rpmbuild(macros) >= 1.330
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ACX100 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%package -n kernel%{_alt_kernel}-net-acx100
Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-net-acx100
This is driver for WLAN card based on ACX100 for Linux.

%description -n kernel%{_alt_kernel}-net-acx100 -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%package -n kernel%{_alt_kernel}-smp-net-acx100
Summary:	Linux SMP driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-smp-net-acx100
Linux SMP driver for WLAN card base on ACX100.

%description -n kernel%{_alt_kernel}-smp-net-acx100 -l pl
Sterownik dla Linuksa SMP do kart bezprzewodowych na uk³adzie ACX100.

%prep
%setup -q -c
%patch0 -p1

%build
%build_kernel_modules -m acx

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m acx -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-acx100
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-acx100
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-acx100
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-acx100
%depmod %{_kernel_ver}smp

%files -n kernel%{_alt_kernel}-net-acx100
%defattr(644,root,root,755)
%doc Changelog README
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp}
%files -n kernel%{_alt_kernel}-smp-net-acx100
%defattr(644,root,root,755)
%doc Changelog README
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
