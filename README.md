
## Description

This Python script collects all necessary details for your virtual machines (VMs) deployed on Nutanix infrastructure and organizes them into a single Excel file.

It will retrieve the following information for each VM: "VM name", "description", "Memory(GiB)", "vCPU", "Number of disks", "total storage(GiB)", "Subnets", "IP address", "NGT Status", "OS", "Power State", "Host", "Cluster", "Creation Time", "categories", and "VM efficiency" 
nb: the script won't retrieve (VM efficiency) if your cluster has a licensing violation. 

## Usage

1. Clone this repo locally:
   ```bash
   git clone https://github.com/elyacoub9/NTNX-VMs-Infos.git
   ```
   ```bash
   cd NTNX-VMs-Infos
   ```

2. Install the required modules:
   ```bash
   pip install -r requirements.txt
   ```

3. Run your script:
   ```bash
   py VM_infos.py
   ```

## TODO
- add error handling (Failing Silently)


