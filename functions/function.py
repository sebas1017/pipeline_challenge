import requests
from bs4 import BeautifulSoup

def obtener_datos_delegaciones():
	lista_url = obtener_url()
	datos = obtener_data_delegados(lista_url)
	return datos 


def obtener_url():
	r = requests.get('https://www.archivo.cdmx.gob.mx/gobierno/delegaciones')
	lista = []
	if r.status_code == 200:
		soup = BeautifulSoup(r.content,'html.parser')
		datos = soup.find_all('div',attrs={"class":"Panel-accordion--simple"})
		for i in datos:
			d = i.find('div',attrs={"class":"Link-viewfull"}).find('a').get('href')
			url = f"https://www.archivo.cdmx.gob.mx/{d}"
			lista.append(url)  
	return lista

def obtener_data_delegados(lista):
	data = []
	for i in lista:
		dic = {}
		r = requests.get(i)
		soup = BeautifulSoup(r.content,'html.parser')
		codigo_postal = soup.find_all('div',attrs={"class":"Panel-credential"})[1].find_all('div',attrs={"class":"Panel-credential-data"})[3].text.replace("Código Postal:","").strip().rstrip().split("–")
		codigo_postal = [i.strip().rstrip() for i in codigo_postal]
		dic["delegacion"] = soup.find('div',attrs={"class":"Title-0"}).text.strip().rstrip()
		dic["alcalde"] = soup.find('div',attrs={"class":"Panel-credential-holder"}).text.replace("Titular:","").replace("\n","").strip().rstrip()
		dic["codigo_inicial"] = codigo_postal[0]
		dic["codigo_final"] = codigo_postal[1]		
		data.append(dic)
	return data 
		





