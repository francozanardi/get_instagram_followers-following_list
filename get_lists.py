from requests import get
from json import dumps
from time import sleep
import os


#Obtiene el ID a partir de un username, en caso de error retorna una cadena de texto vacía.
def get_id(username, cookies):
	resp = get("https://www.instagram.com/" + username + "/?__a=1", cookies = cookies)
	
	if(resp.status_code == 200):
		return resp.json()["graphql"]["user"]["id"]

	return ""

def ig_request(hash_id, variables, resolver, resolver_args = {}, cookies = {}, sleep_requests = 5, sleep_error = 10, reintentos = 3):
	has_next_page = True
	reintentos_actuales = 0
	
	params = {
		"query_hash": hash_id,
		"variables": dumps(variables)
	}
	
	while(has_next_page and reintentos_actuales < reintentos):
		resp = get("https://www.instagram.com/graphql/query/", params = params, cookies = cookies)
		
		if(resp.status_code == 200):
			reintentos_actuales = 0

			try:
				has_next_page = resolver(variables, resp.json(), resolver_args);
				
				if(has_next_page):
					params["variables"] = dumps(variables)
					sleep(sleep_requests)
			except Exception as err:
				print("Se prudujo un error en el resolver:", err)
				reintentos_actuales = reintentos #si se produjo un error salimos del bucle inesperadamente
			
		else:
			reintentos_actuales += 1
			
			print("Se ha producido un error en la petición, estamos realizando el reintento %d de %d reintentos posibles." % (reintentos_actuales, reintentos))
			
			sleep(sleep_error)
			
	
	return reintentos_actuales < reintentos	


count_followers = 0
def resolver_followers(variables, data_resp, extra_args):
	global count_followers
	
	data_resp = data_resp["data"]["user"]["edge_followed_by"]
	
	#iteramos sobre los usuarios que obtuvimos
	for node in data_resp["edges"]:
		node = node["node"]
		count_followers += 1
		
		print("[%d/%d] %s" % (count_followers, data_resp["count"], node["username"]))
	
	if(data_resp["page_info"]["has_next_page"]):
		variables["after"] = data_resp["page_info"]["end_cursor"]
		return True
		
	return False
		
def get_followers_list(id, cookies):
	variables = {
		"id": id,
		"first": 50
	}
	
	return ig_request("c76146de99bb02f6415203be841dd25a", variables, resolver_followers, cookies = cookies)


count_following = 0
def resolver_following(variables, data_resp, extra_args):
	global count_following

	data_resp = data_resp["data"]["user"]["edge_follow"]
	
	#iteramos sobre los usuarios que obtuvimos
	for node in data_resp["edges"]:
		node = node["node"]
		count_following += 1
		
		print("[%d/%d] %s" % (count_following, data_resp["count"], node["username"]))
	
	if(data_resp["page_info"]["has_next_page"]):
		variables["after"] = data_resp["page_info"]["end_cursor"]
		return True
		
	return False

def get_following_list(id, cookies):
	variables = {
		"id": id,
		"first": 50
	}
	
	return ig_request("d04b0a864b4b54837c0d870b0e77e076", variables, resolver_following, cookies = cookies)

def parse_args():
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--username', type=str, required=True, help="Target username.")
	parser.add_argument('-s', '--sessionid', type=str, required=True, help="sessionid cookie (from an open Instagram account).")
	
	return parser.parse_args()

args = parse_args()

cookies = {
	"sessionid": args.sessionid
}

id = get_id(args.username, cookies)
while(id == ""):
	print("No se ha podido obtener el ID del usuario.")
	print("Reintentando en 5 segundos...")
	sleep(5);
	
	id = get_id(args.username, cookies)
	
print("ID obtenida:", id)

print("\nLista de seguidores:\n")
if(not get_followers_list(id, cookies)):
	print("Se ha producido un error al obtener la lista de seguidores de %s." % (args.username))
	
print("\n" + "-"*50 + "\n")

print("Lista de seguidos:\n")
if(not get_following_list(id, cookies)):
	print("Se ha producido un error al obtener la lista de seguidos por %s." % (args.username))

	