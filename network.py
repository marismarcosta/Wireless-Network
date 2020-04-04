from host import host
from package import package
from link import link_layer
from physical import physical_layer
from table import routing_table

class network_layer:
	def __init__(self,host):
		self.host = host
		self.table = routing_table()
		self.pending_pck = []

	def send_pck():	#to link layer
		pass

	def receive_pck(self,pck):	#receive a package from link layer
		if(pck.get_originator() == self.host.get_mac()): #if the receptor is the package originator
			return	#ignore the package

		if((pck.get_type() == 'RREP' or pck.get_type() == 'DATA') and pck.get_next() != self.host.get_mac()):
			return #ignore the package

		if(not self.add_received_pck(pck)):	#add the package to the received list and check
			return #ignore the package if it already in the list

		if(pck.get_type() == 'DATA' and pck.get_destination() = self.host.get_mac()): #if the receptor is the package destination
			pck.get_contents() #receive contents of the package
			#IMPORTANT: write it in a log file

		elif(pck.get_type() == 'DATA' and pck.get_destination() != self.host.get_mac()): #if the receptor is next at the route
			if(self.table.check_route(pck.get_destination())) #check if there is a route
				pck.add_next(self.table.get_next_to(pck.get_destination())):	#add next to the route
				self.host.link.sending_request(pck)				
			else:	#if there is not a route in routing table
				pck.add_next([]) #send a RREQ package to all neighbors
				self.create_RREQ_pck(pck)

		elif(pck.get_type() == 'RREQ' and pck.get_destination() != self.host.get_mac()): #if the package is RREQ e the receptor is not the destination
			pck.add_path(self.host.get_mac())
			neighbor_position = len(pck.get_path()) - 2
			if(neighbor_position < (len(pck.get_path()) - 1)):
				path = pck.get_path()
				neighbor = path[neighbor_position]
				if(self.host.is_reacheable(neighbor)):	#check and if its reacheable 
						self.table.save_route(path)	#save the route
						self.check_send() #check the route to send
				self.host.link.sending_request(pck)	#send the package to link layer


		elif(pck.get_type() == 'RREQ' and pck.get_destination() == self.host.get_mac()): #if the package is RREQ e the receptor is the destination
			pck.add_path(self.host.get_mac())
			pck_RREP = create_RREP_pck(pck)
			neighbor_position = 1
			if(neighbor_position < (len(pck.get_path()) - 1)):
				path = pck_RREP.get_path()
				neighbor = path[neighbor_position]
			else:
				neighbor = []
			#CONTINUAR DAQUI!!!!!!!


		elif(pck.get_type() == 'RREP' and pck.get_destination() != self.host.get_mac()): #if the package is RREP e the receptor is not the destination
			count = 0
			host_position = -1
			for obj in pck.get_path():	#check the host position in the path
				if(obj == self.host.get_mac()):	
					host_position = count #when it is found, save it
					break
				count += 1
			if(host_position < 0):	#if the receptor host is not in the path
				pck.add_next([]) #send a RREQ package to all neighbors
				self.create_RREQ_pck(pck)
			else:	#if the receptor is in the path
				if(host_position < (len(pck.get_path()) - 1)):
					path = pck.get_path()
					neighbor = path[host_position+1]	#get next host in the path
					if(self.host.is_reacheable(neighbor)):	#check and if its reacheable 
						self.table.save_route(path)	#save the route
						self.check_send() #check the route to send
						pck.add_next(neighbor)	#add the neighbor as next
						self.host.link.sending_request(pck)	#send the package to link layer
				else:	#if the next host is not save in the path
					pck.add_next([]) #send a RREQ package to all neighbors
					self.create_RREQ_pck(pck)

		elif(pck.get_type() == 'RREP' and pck.get_destination() == self.host.get_mac()): #if the package is RREP e the receptor is the destination
			self.table.save_route(pck.get_path()) #save the route
			self.check_send()	#check the route and send the package			


	def check_send(self):
		for i in range(len(self.pending_pck)):	#check all pending packages that wait for a route
			pck = self.pending_pck[0]
			if(self.table.check_route(pck.get_destination())) #if there is a route to destination host
				pck.add_next(self.table.get_next_to(pck.get_destination()))	#get the next in routing table and add to package
				self.host.link.sending_request(pck) #send the package to link layer
				self.pending_pck.pop(0)	#remove the package from the list
			else:	#if there is no route to destination in routing table 
				self.pending_pck.pop(0)	#remove the package from the list
				self.pending_pck.append(pck)	#add the first package to the end of a list
				

	def add_received_pck(self,pck):
		pass

	def function():
		pass