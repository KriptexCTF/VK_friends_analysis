import matplotlib.pyplot as plt
import networkx as nx
import time
from vk_api import *

def get_name_vk(id):
	user_get = (vk.users.get(user_ids=id))[0]
	string = user_get['last_name'] + ' ' + user_get["first_name"]
	user_dict[id] = string
	print(string + '\nid: ' + str(id) + '\n' + '-'*30)
	return (string + '\nid: ' + str(id))
def id_to_name(id):
	name = user_dict[id]
	string = name + '\nid: ' + str(id)
	return string
def find_linked(edges, arr):
	for user in range (len(arr)):
		groups = 0
		user_id = arr[user][2]
		for k in range(user+1, len(arr)):
			for group_id in range (len(arr[user][3])):
				if(arr[user][3][group_id] in arr[k][3]):
					groups += 1
				if((groups >= 3) and (user_id in arr[k][4])):
					edges.append((id_to_name(user_id),id_to_name(arr[k][2])))
					break
	return edges

try:
	access_token = ""
	access_token = open("token", 'r').read()
except FileNotFoundError:
	print("Token file not found!")
while(access_token == ""):print("Enter valid access_token!");access_token = input(":>");open("token", "w").write(access_token)
vk_session = vk_api.VkApi(token=access_token)
try:
	vk = vk_session.get_api()
	nickname = input("Enter nickname: ")
	main_id = vk.utils.resolveScreenName(screen_name=nickname)['object_id']
	friends = vk.friends.get(user_id=main_id)
except ApiError:
	open("token", "w").write("")
	print("Token not valid!")
	exit()
except OSError:
	print("No enternet connection!\nOR raise limit")
	exit()
arr, nodes, edges = [], [], []
user_dict = {}
nodes.append(get_name_vk(main_id))
for id in friends['items']:
	time.sleep(0.5)
	user_get = vk.users.get(user_ids=(id))
	user_get = user_get[0]
	try:
		user_friends = (vk.friends.get(user_id=id))['items']
		group_get = vk.groups.get(user_id=id)
		group_arr = []
		user_dict[id] = f"{user_get['last_name']} {user_get['first_name']}"		
		nodes.append(id_to_name(id))
		arr.append([user_get["last_name"], user_get["first_name"], id, group_get['items'], user_friends])
		edges.append((id_to_name(main_id),id_to_name(id)))
	except ApiError:
		print(f"WARNING: {user_get['last_name']} {user_get['first_name']} id:{id} private account!")
arr = sorted(arr)
G = nx.Graph()
G.add_nodes_from(nodes)
edges = find_linked(edges, arr)
G.add_edges_from(edges)
pos = nx.spring_layout(G)
pos[main_id] = [0, 0]
nx.draw(G, pos, with_labels=True, node_size=100, node_color='green', font_weight='bold', font_color='red')
try:
	plt.show()
except KeyboardInterrupt:
	print("\nExit")
	exit()
