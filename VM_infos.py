import requests
from datetime import datetime
import urllib3
from openpyxl import Workbook
from openpyxl.styles import Font


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = input("your PC user name: ")
password = input("your PC Password: ")
pc_ip =input("your PC ip: ")

url = f'https://{pc_ip}:9440/api/nutanix/v3/vms/list'

payload = { }

headers = {'Content-Type': "application/json" }

auth = (username, password)

response = requests.post(url, json=payload, headers=headers, auth=auth,verify=False)

response.status_code == 200
data = response.json()

entities=data["entities"]
print(len(entities))
vms_infos=[]
 
for entity in entities:
    
    status=entity["status"]
    metadata=entity["metadata"]


    def vm_name_desc(Name_Or_Desc):
        if Name_Or_Desc=="Name":
            name=status["name"]
            return name

        elif Name_Or_Desc=="Desc":
            if "description" in status.keys():
                description=status["description"]
                return description
            else:
                return None

    def vm_ram_cpu(RAM_or_CPU):
        if RAM_or_CPU=="CPU":
            vcpu=status["resources"]["num_sockets"]
            return vcpu
        elif RAM_or_CPU=="RAM":
            ram=status["resources"]["memory_size_mib"]
            ram=ram//1024
            return ram

    def vm_disks(nb_or_totalcapacity):
        if nb_or_totalcapacity=="nb":
            nb=0
            for disk in status["resources"]["disk_list"]:
                if disk["device_properties"]["device_type"]=="DISK":
                    nb+=1
                else:
                    continue
            return nb
        elif nb_or_totalcapacity=="totalcapacity":
            totalcapacity=0
            for disk in status["resources"]["disk_list"]:
                if disk["device_properties"]["device_type"]=="DISK":
                    disksize=int(disk["disk_size_mib"]/1024)
                    totalcapacity+=disksize

            return totalcapacity

    def vm_net(subnet_or_ip):
        subnets_names=[]
        ips=[]
        nic_list=status["resources"]["nic_list"]
        results=""
        if len (nic_list):
            for nic in nic_list:

                if subnet_or_ip=="subnet":
                    subnet_name=nic["subnet_reference"]["name"]
                    subnets_names.append(subnet_name)
                    result_list=subnets_names

                if subnet_or_ip=="ip":
                    if nic["ip_endpoint_list"] :
                        ip=nic["ip_endpoint_list"][0]["ip"]
                        ips.append(ip)
                        result_list=ips
                    else:
                        return None
                    
            for result in result_list:
                if len(result_list)==1:
                    results=result_list[0]
                elif len(result_list)>1:
                    results=results+"\n"+result
            return(results.lstrip())
        else:
            return None


    def vm_ngt(status_or_os):
        if "guest_tools" in status["resources"] :
            ntnx_gest_tools=status["resources"]["guest_tools"]["nutanix_guest_tools"]

            if status_or_os=="status":
                ngt_status=ntnx_gest_tools["ngt_state"]
                return ngt_status
            elif status_or_os=="os":

                os=ntnx_gest_tools["guest_os_version"]
                return os
        else:
            return None

    def vm_powerstate_host(powerstate_or_host):
        power_state=status["resources"]["power_state"]
        if powerstate_or_host == "powerstate":
            return power_state

        if powerstate_or_host == "host":
            if power_state=="ON":
                host=status["resources"]["host_reference"]["name"]
                return host
            else:
                return f"{None} (the VM is OFF)"


    def vm_cluster():
        cluster=status["cluster_reference"]["name"]
        return cluster

    def vm_creation_time():
        creation_time=metadata["creation_time"]
        creation_time=datetime.fromisoformat(creation_time)
        creation_time=creation_time.strftime("%Y-%m-%d %H:%M")
        return creation_time

    def vm_categories():
        list_of_categories=[]
        categories_data=metadata["categories"]
        categories=""
        for key, value in categories_data.items():
            list_of_categories.append(f"{key}:{value}")
        

        for category in list_of_categories :
            if len(list_of_categories)==1:
                categories=list_of_categories[0]
            elif len(list_of_categories)>1:
                categories=categories+"\n"+category
                return(categories.lstrip("\n"))
        return(categories)
    

    vm= [vm_name_desc("Name"), vm_name_desc("Desc"),
           vm_ram_cpu("RAM"), vm_ram_cpu("CPU"),
             vm_disks("nb"), vm_disks("totalcapacity"),
                str(vm_net("subnet")), str(vm_net("ip")),
                  vm_ngt("status"), vm_ngt("os"),
                    vm_powerstate_host("powerstate"), vm_powerstate_host("host"),
                    vm_cluster(), vm_creation_time(),
                    str(vm_categories()) ]
    

       
    vms_infos.append(vm)
    #print (row)


wb = Workbook()
ws = wb.active
ws.append(["VM name", "description", "Memory(Gib)", "vCPU", "number of disks", "total storage(Gib)", "Subnets", "IP address", "NGT Status", "OS", "Power State", "Host", "Cluster", "Creation Time", "categories"])

for row in vms_infos:
    
    ws.append(row)

ft = Font(bold=True)
for row in ws["A1:O1"]:
    for cell in row:
        cell.font = ft

wb.save("NTNXvminfos.xlsx")



