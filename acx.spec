#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
# TODO:
# - UP/SMP scheme, pass CC and CFLAGS
%define		_orig_name	acx100_pci

Summary:	Linux driver for WLAN card base on ACX100
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie ACX100
Name:		kernel-net-acx100
Version:	0.2.0pre6_plus_fixes_7
%define	_rel	0.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://rhlx01.fht-esslingen.de/~andi/acx100/acx100-%{version}.tar.bz2
# Source0-md5:	d03a9252ad411bd77eeb508a34bca8bd
URL:		http://acx100.sourcefroge.net/index.html
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.4.0}}
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-net-acx100
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ACX100 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad ACX100.

%prep
%setup -q -c

%build
%{__make} -C acx100-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install acx100-%{version}/src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
#%doc readme
/lib/modules/%{_kernel_ver}/misc/*
