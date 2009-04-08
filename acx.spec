# TODO:
# - add firmware download?
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Linux driver for WLAN card base on ACX100/ACX111
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych na układzie ACX100/ACX111
Name:		acx
Version:	20070101
%define	_rel	3
Release:	%{_rel}
License:	MPL or GPL
Group:		Base/Kernel
Source0:	http://www.cmartin.tk/acx/%{name}-%{version}.tar.bz2
# Source0-md5:	ec6322b9c82781897a9433ef0cefda6f
Patch0:		%{name}-skb.patch
# based on https://dev.openwrt.org/browser/trunk/package/acx/patches/003-2.6.24-compat.diff?rev=10425&format=txt
Patch1:		%{name}-2.6.24.patch
Patch2:		%{name}-2.6.29.patch
URL:		http://acx100.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
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
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel%{_alt_kernel}-net-acx100

%description -n kernel%{_alt_kernel}-net-acx
This is driver for WLAN card based on ACX100/ACX111 for Linux.

%description -n kernel%{_alt_kernel}-net-acx -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ ACX100/ACX111.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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

%files -n kernel%{_alt_kernel}-net-acx
%defattr(644,root,root,755)
%doc Changelog README
/lib/modules/%{_kernel_ver}/misc/*.ko*
