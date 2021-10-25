## Virtualization requirements
- **equivalence**
	- VMM behaves as running on its own HW
- **resource control**
	- VM has full control of its virtualized resources
- **performance**
	- 99% of instruction natively, executed without VMM interrupt

## History
### VMWare
- around 2000
- **problems with early x86 CPUs**
	- early intel CPUs didn't have virtualization support
	- knowledge of privileged/unprivileged execution must be known by the compiler
	- solved by JIT compilation of problematic instructions - hard
		- performance hit

- **paravirtualization**
	- 2003 Xen
	- modification of guest OS kernel
		- very costly

### Early hw virtualization support
- 2005 - Intel VT-x
- 2006 - AMD-V

## True virtualization
- no paravirtualization
- guest cannot know it's virtualized


## VMM implementation (today)
- critical (lower) kernel parts paravirtualized
	- VM kernel calls hypervisor, not HW directly
	- in practice handleled by implanting virtual device drivers
- **Hypervisior (VMM)**
	- creates illusion of dedicated machine HW for each VM
	- illusion not perfect, difficult parts handled by VM controller OS
- **separately running VM Controller OS**
	- VM controller - administrator contol

### Virtual device drivers
- supports fast communication infrastructure

### Containerization + virtualization combined

### True virtualization
![[Pasted image 20211020161622.png]]
- misleading
![[Pasted image 20211020161820.png]]

- user processes run natively
- ![[Pasted image 20211020161943.png]]


### Compression of privileges
- kernels wants to run in level 0
	- but level 0 should be only hypervisor
- **Intel/AMD root/non-root modes**
	- hypervisior runs with additional root-mode CPU flag
- **User -> Kernel**
	- kernel VM syscalls run natively
	- some software interrupts (div-by-zero, debugger interrupts) also native
- **User/Kernel -> Hypervisor**
	- VM exit event -> switch to hypervisor
	- other software (synchronous) interrupts (page faults)
	- asynchronous  hardware interrupts - may not be related to VM, must be handeled by hypervisor
		- disk device interrupts - handled by VM associated with the disk
		- timer interrupts - used for VM guest scheduling
			- must be also delivered to each VM kernel for their own process scheduling
- privileged/unprivileged CPU registers
	- CPU HW supporting access control
- VM exit
	- state of CPU saved to RAM (CPU cache today), loaded hypervisor CPU state

### Memory virtualization
- normally - page table, cached in TLB
	- TLB fault - CPU accesses page table
	- page table fault -> kernel wakeup
- in VM - another mapping layer needed
	- virtualized physical address space of guest mapped to the real physical address space
- **nested page table**
	![[Pasted image 20211020165938.png]]
	
### I/O virtualization
- naive mode - each I/O op. ends up in hypervisor
	- exclusive access (not common)
	- shared mode - virt. I/O devices in hypervisor for each VM guest
		- emulated, slow
- virtual I/O device drivers implanted in guest, paravirtualization
- IOMMU
	- device support for shared mode
	- skip hypervisor altogether

