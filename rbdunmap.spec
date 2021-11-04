#
# spec file for package rbdunmap
#

Name:           rbdunmap
Version:        1.0
Release:        1%{?dist}
Group:          System/Filesystems
Summary:        Ceph unmap service for containerd
# License:        GPL-3.0-or-later
License:        GPLv3+

BuildArch:      noarch

Requires:       ceph-common >= 15.2.8
Requires:       systemd


%description
Ceph unmap service for containerd
# When using a specific version of K8S with containerd, a software reboot or
# power-off is not possible. It should proceed in the order of container
# shutdown -> filesystem umount -> rbd unmap, but it cannot to be done.
# The kernel umounts only the default namespace, and does not umount the
# filesystem of the namespace where the container bind-mount is mounted.
# As a result, rbd is still state of device busy and cannot be unmapped.
# This service is summoned before terminating kernel, unmapping rbd with
# force option, so helps kernel can be well terminated.


%prep
# %autosetup -p1


%build
# nothing to build


%install
install -m 0755 ./rbdunmap /usr/bin/
install -m 0755 ./rbdunmap.service /usr/lib/systemd/system/


%post
/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable rbdunmap &> /dev/null || :
/bin/systemctl --system start rbdunmap &> /dev/null || :


%preun
echo "You may not use rbd-PVC based Pods from now on."
echo "Check your rbd-PVC based Pods."


%postun
rm /usr/bin/rbdunmap
rm /usr/lib/systemd/system/rbdunmap.service
/bin/systemctl --system daemon-reload &> /dev/null || :


%files
/usr/lib/systemd/system/rbdunmap.service
/usr/bin/rbdunmap


%attr(0755,root,root) %dir %{_localstatedir}/log/rbd-target-gw
%attr(0755,root,root) %dir %{_localstatedir}/log/rbd-target-api
