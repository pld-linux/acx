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
Version:	0.2.0pre4
%define	_rel	0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://rhlx01.fht-esslingen.de/~andi/acx100/acx100-0.2.0pre4.tar.bz2
# Source0-md5:	cc4e97d866116af36f24b1c52db8e4a8
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
%{__make} -C acx100-0.2.0pre3

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install acx100-0.2.0pre3/src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

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
