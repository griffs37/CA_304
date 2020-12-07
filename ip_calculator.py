#!usr/bin/env python

# Name: Stephen Griffin
# Student ID: 18482934

# ip_addr = string ipv4 eg "136.206.18.7"

def get_class_stats(ip_addr):
	
	byte1 = to_binary(ip_addr)[0]  #convert th first byte to binary to check the bits
	
	if byte1[0] == "0":
		print("-" * 40 + "\nClass: A" + "\n" + "Network: 128" + "\n" + "Host: 16777216" + "\n" + "First address: 0.0.0.0" + "\n" + "Last address: 127.255.255.255\n" + "-" * 40)  #adding the "-" * 40 for formatting/spacing output
	
	elif byte1[1] == "0":
		print("-" * 40 + "\nClass: B" + "\n" + "Network: 16384" + "\n" + "Host: 65536" + "\n" + "First address: 128.0.0.0" + "\n" + "Last address: 191.255.255.255\n" + "-" * 40)
	
	elif byte1[2] == "0":
		print("-" * 40 + "\nClass: C" + "\n" + "Network: 2097152" + "\n" + "Host: 256" + "\n" + "First address: 192.0.0.0 " + "\n" + "Last address: 223.255.255.255\n" + "-" * 40)
	
	elif byte1[3] == "0":
		print("-" * 40 + "\nClass: D" + "\n" + "Network: N/A" + "\n" + "Host: N/A" + "\n" + "First address: 224.0.0.0 " + "\n" + "Last address: 239.255.255.255\n" + "-" * 40)
	
	elif byte1[4] == "0":
		print("-" * 40 + "\nClass: E" + "\n" + "Network: N/A" + "\n" + "Host: N/A" + "\n" + "First address: 240.0.0.0 " + "\n" + "Last address: 255.255.255.255\n" + "-" * 40)

def to_binary(ip_addr):
	split = ip_addr.split(".")  #split string on the dots
	return ['{0:08b}'.format(int(x)) for x in split]  #turn the string into an int and put into binary

def to_decimal(ip_addr_list):
	return ".".join([str(int(x, 2)) for x in ip_addr_list])  #for each byte in the list convert to int and join all


def get_subnet_stats(ip_addr, subnet_mask):
	subnet_binary = to_binary(subnet_mask)  #convert the subnet to binary
	subnet_join = "".join(subnet_binary)  # join the binary values
	binarys = list(subnet_join) # create a list of the binary digits
	subnet_split = subnet_mask.split(".") #split the values on the dot

	count = 0        # check the 1's and increment 
	for i in binarys:
		if i == "1":
			count +=1
	
	byte_check = to_binary(ip_addr)[0]

	if byte_check[0:3] != "110" and byte_check[0:2] != "10":

		return "Please enter a Class C or B address..."


	if subnet_split[2] == "255" :     # check if the ip is class C, if not move to the elif for class B 
		
		subnet_bits = 0   #check the subnet bit count
		for i in subnet_binary[3]:
			if i == "1":
				subnet_bits +=1
		subnets = 2 ** subnet_bits

		unmasked_bits = 0   # check the unmasked bit count
		for i in subnet_binary[3]:
			if i == "0":
				unmasked_bits +=1 
		hosts = (2**unmasked_bits)-2  # Find number of hosts by putting 2 to the power of unmasked bits and subtracting 2

		block_size = 256 - int(subnet_split[3])  # find the block size by subtracting the subnet from 256

		valid_subnets_clean = []  # a list for the valid subnets with cleaned formatting
		valid_subnets = [ip_addr for x in range(4)]
		valid_subnets = [x.split(".") for x in valid_subnets]
		
		for index, item in enumerate(valid_subnets):
			valid_subnets[index][3] = str(int(valid_subnets[index][3]) + (block_size * index))
		for i in valid_subnets:
			valid_subnets_clean.append(".".join(i))  # clean up the list
		

		broadcast_clean = []
		broadcast = list(valid_subnets)
		i = 0
		while i < len(broadcast) -1:
			broadcast[i][3] = str(int(broadcast[i+1][3]) - 1)
			i += 1
		broadcast[3][3] = "255"
		for i in broadcast:
			broadcast_clean.append(".".join(i))  #clean up the list

		first_addr_clean = []
		first_addr = list(valid_subnets_clean)
		first_addr = [x.split(".") for x in first_addr]
		
		for index, item in enumerate(first_addr):
			first_addr[index][3] = str(int(first_addr[index][3]) + 1)
		for i in first_addr:
			first_addr_clean.append(".".join(i))  # clean up the list

		last_addr_clean = []
		last_addr = list(broadcast)
		for index, item in enumerate(last_addr):
			last_addr[index][3] = str(int(last_addr[index][3]) - 1)
		for i in last_addr:
			last_addr_clean.append(".".join(i))

		print("Address: {}/{}\nSubnets: {}\nHosts: {}\nValid subnets: {}\nBroadcast addresses: {}\nFirst addresses: {}\nLast addresses: {}\n{}".format(ip_addr, count, subnets, hosts, valid_subnets_clean, broadcast_clean, first_addr_clean, last_addr_clean, "-" * 40))

	else:    #if the ip is class B
		subnet_bits = 0   #subnet bit count
		
		for i in subnet_binary[2]:
			if i == "1":
				subnet_bits +=1
		subnets = 2 ** subnet_bits

		unmasked_bits = 0   # check the unmasked bit count
		byte3_4 = subnet_binary[3] + subnet_binary[2] #concatenate the bytes to check the overall bits
		for i in byte3_4:
			if i == "0":
				unmasked_bits +=1

		hosts = (2**unmasked_bits)-2  # Find number of hosts by putting 2 to the power of unmasked bits and subtracting 2

		if subnet_split[2] == "255":
			block_size = 256 - int(subnet_split[-1])  # find the block size by subtracting the subnet from 256
		
		else:
			block_size = 256 - int(subnet_split[2])
		
		# operations for valid subnet calculation
		valid_subnets_clean = []
		valid_subnets = [ip_addr for x in range(4)]
		valid_subnets = [x.split(".") for x in valid_subnets]
		for index, item in enumerate(valid_subnets):
			valid_subnets[index][2] = str(int(valid_subnets[index][2]) + (block_size * index))  #add the block size by index 
		for i in valid_subnets:
			valid_subnets_clean.append(".".join(i))  # clean up the list

		# operations for first addresses calculations
		first_addr_clean = []
		first_addr = list(valid_subnets_clean)
		first_addr = [x.split(".") for x in first_addr]
		
		for index, item in enumerate(first_addr):
			first_addr[index][3] = str(int(first_addr[index][3]) + 1)
		for i in first_addr:
			first_addr_clean.append(".".join(i))  # clean up the list

		subnet_check = subnet_mask.split(".")

		# operations for broadcast addresses calculations
		broadcast_clean = []
		broadcast = list(valid_subnets)
		i = 0
		if subnet_check[2] != "255":
			while i < len(broadcast) -1:
				broadcast[i][2] = str(int(broadcast[i+1][2]) - 1)
				broadcast[3][2] = str(int(broadcast[2][2]) + block_size)
				broadcast[i][3] = "255"
				i += 1
				broadcast[i][3] = "255"
		else:
			i = 0
			while i < len(broadcast):
				broadcast[i][3] == str(int(broadcast[i-1][3]) + block_size)
				i += 1
			broadcast[0][3] == str(block_size - 1)
		
		for i in broadcast:
			broadcast_clean.append(".".join(i))  #clean up the list
		

		last_addr_clean = []
		last_addr = list(broadcast)
		for index, item in enumerate(last_addr):
			last_addr[index][3] = str(int(last_addr[index][3]) - 1)
		for i in last_addr:
			last_addr_clean.append(".".join(i))


		print("Address: {}/{}\nSubnets: {}\nAddressable hosts per subnet: {}\nValid subnets: {}\nBroadcast Addresses: {}\nFirst Addresses: {}\nLast Addresses: {}\n{}".format(ip_addr, count, subnets, hosts, valid_subnets_clean, broadcast_clean, first_addr_clean, last_addr_clean, "-" * 40))


def get_supernet_stats(ip_listc):
	
	binary1 = "".join(to_binary(ip_listc[0])) #convert to binary and join them
	binary2 = "".join(to_binary(ip_listc[1]))
	binary3 = "".join(to_binary(ip_listc[2]))

	i = 0
	count = 0
	while binary1[i] == binary2[i] and binary1[i] == binary3[i] and binary2[i] == binary3[i]:
		count +=1
		i +=1

	mask = "1" * count + binary1[count:]
	masks = []
	
	for i in range(4):
		masks.append(mask[:8])
		mask = mask[8:]

	mask = to_decimal(masks)
	
	print("Address: {}/{}\nNetwork Mask: {}\n{}".format(ip_listc[0], count, mask, "-" * 40))


def main():
	get_class_stats("136.206.18.7")
	get_subnet_stats("192.168.10.0","255.255.255.192")  #testing 
	get_supernet_stats(["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"])

main()