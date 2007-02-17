# TODO:
# - add firmware download?
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
#
%ifarch sparc
%undefine	with_smp
%endif
#
Summary:	Linux driver for WLAN card base on ACX100/ACX111
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych na układzie ACX100/ACX111
Name:		acx
Version:	20070101
%define	_rel	2
Release:	%{_rel}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://www.cmartin.tk/acx/%{name}-%{version}.tar.bz2
# Source0-md5:	ec6322b9c82781897a9433ef0cefda6f
URL:		http://acx100.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.16}
BuildRequires:	rpmbuild(macros) >= 1.330
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ACX100/ACX111 for Linux.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ ACX100/ACX111.

%package -n kernel%{_alt_kernel}-net-acx
Summary:	Linux driver for WLAN card base on ACX100/ACX111
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych na układzie ACX100/ACX111
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Obsoletes:	kernel%{_alt_kernel}-net-acx100
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-net-acx
This is driver for WLAN card based on ACX100/ACX111 for Linux.

%description -n kernel%{_alt_kernel}-net-acx -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ ACX100/ACX111.

%package -n kernel%{_alt_kernel}-smp-net-acx
Summary:	Linux SMP driver for WLAN card base on ACX100/ACX111
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart bezprzewodowych na układzie ACX100/ACX111
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Obsoletes:	kernel%{_alt_kernel}-smp-net-acx100
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-smp-net-acx
Linux SMP driver for WLAN card base on ACX100/ACX111.

%description -n kernel%{_alt_kernel}-smp-net-acx -l pl.UTF-8
Sterownik dla Linuksa SMP do kart bezprzewodowych na układzie ACX100/ACX111.

%prep
%setup -q

%build
%build_kernel_modules -m acx

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m acx -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-acx
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-acx
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-acx
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-acx
%depmod %{_kernel_ver}smp

%if %{with up}
%files -n kernel%{_alt_kernel}-net-acx
%defattr(644,root,root,755)
%doc Changelog README
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif

%if %{with smp}
%files -n kernel%{_alt_kernel}-smp-net-acx
%defattr(644,root,root,755)
%doc Changelog README
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
