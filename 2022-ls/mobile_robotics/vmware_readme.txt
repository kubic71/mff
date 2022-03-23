modprobe -a vmw_vmci vmmon

==> Before using VMware, you need to reboot or load vmw_vmci and vmmon kernel modules (in a terminal on root: modprobe -a vmw_vmci vmmon)
==> You may also need to enable some of the following services:
- vmware-networks: to have network access inside VMs
- vmware-usbarbitrator: to connect USB devices inside VMs
These services can be activated during boot by enabling .service units or only when a VM is started by enabling .path units.
