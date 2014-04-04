#Tarea1 exploratorio
import json
from urllib.request import urlopen

def output(fb_id, token):

    request_persona = "https://graph.facebook.com/" + fb_id +"?fields=name,picture.width(400).height(400)"
    fb_persona_encoded = urlopen(request_persona)
    fb_persona_encoded2 = fb_persona_encoded.read()
    fb_persona_decoded = json.loads(fb_persona_encoded2.decode('utf8'))

    request = "https://graph.facebook.com/" + fb_id + "/friends?fields=name,birthday,gender,location,relationship_status,languages&access_token=" + token
    fb_info_encoded = urlopen(request)
    fb_info_encoded2 = fb_info_encoded.read()
    fb_info_decoded = json.loads(fb_info_encoded2.decode('utf8'))

    generar = {}

    generar['name'] = fb_persona_decoded['name']
    generar['picture'] = {'url': fb_persona_decoded['picture']['data']['url'], 'width': fb_persona_decoded['picture']['data']['width'], 'height': fb_persona_decoded['picture']['data']['height']}

    amigos = {}
    amigos['count'] = len(fb_info_decoded['data'])

    #variables necesarias:
    #para gender:
    male = 0
    female = 0
    #para age:
    cont_edades = 0
    s_edades = 0
    edad_mayor = 0
    edad_menor = 0
    #para idiomas:
    idiomas = []
    hablantes = []
    #para relaciones:
    estados = ["Single","In a relationship","Engaged","Married","In an open relationship","It's complicated","Separated","Divorced","Widowed"]
    n_estados = [0,0,0,0,0,0,0,0,0]
    #para cuidades:
    ciudades = []
    n_ciudades= []
    
    for i in fb_info_decoded['data']:
        cosas = i.keys()
        for i2 in cosas:
            if i2 == 'gender':
                if i['gender'] == 'male':
                    male += 1
                else:
                    female += 1
            if i2 == 'birthday':
                cumple = i['birthday']
                if len(cumple) > 5:
                    cont_edades += 1
                    año = int(cumple[6:10])
                    edad = 2013 - año
                    s_edades += edad
                    if cont_edades == 1:
                        edad_mayor = edad
                        edad_menor = edad
                    else:
                        if edad > edad_mayor:
                            edad_mayor = edad
                        if edad < edad_menor:
                            edad_menor = edad
            
            if i2 == 'languages':
                for i3 in i['languages']:
                    cont = 0
                    for i4 in idiomas:
                        if i3['name'] == i4:
                            hablantes[cont] = hablantes[cont] + 1
                            break
                        cont += 1
                    if len(idiomas) == cont:
                        idiomas += [i3['name']]
                        hablantes += [1]                      

            if i2 == 'relationship_status':
                cont2 = 0
                for i5 in estados:
                    if i['relationship_status'] == i5:
                        n_estados[cont2] = n_estados[cont2] + 1
                        break
                    cont2 += 1
                
                
            if i2 == 'location':
                cont3 = 0
                for i7 in ciudades:
                    if i['location']['name'] == i7:
                        n_ciudades[cont3] = n_ciudades[cont3] + 1
                        break
                    cont3 += 1
                if cont3 == len(ciudades):
                    ciudades += [i['location']['name']]
                    n_ciudades += [1]

                         
    promedio_edades = (s_edades // cont_edades)
    if s_edades % cont_edades > cont_edades//2:
        promedio_edades += 1

    lista_idiomas = []
    for aux1 in range(0,len(idiomas)):
        lista_idiomas += [{'language': idiomas[aux1], 'count': hablantes[aux1]}]
        
    relaciones = {}
    for aux2 in range(0,len(estados)):
        relaciones[(estados[aux2])] = n_estados[aux2]

    lista_ciudades = []
    for aux3 in range(0,len(ciudades)):
        lista_ciudades += [{'town': ciudades[aux3], 'count': n_ciudades[aux3]}]
    
    amigos['gender'] = {'male': male, 'female': female}
    amigos['age'] = {'average': promedio_edades,'youngest': edad_menor, 'oldest': edad_mayor} 
    amigos['languages'] = lista_idiomas    
    amigos['relationship_status'] = relaciones  
    amigos['hometown'] = lista_ciudades
    
    
    generar['friends'] = amigos
    
    generar_encoded = json.dumps(generar)
    return(generar_encoded)

    


fb_id = "1173766522" 
token = "CAACEdEose0cBAIZB1G8ZCuFSQgnfhXyT3ae5yaSzNYYH4IAmZAvn7YNm49d4OgZA8ZCrQ9uvKZCZBzrP7Prs7l73oyvVIzZCzjDZAPoIAMWMu1fsF8MLoKc9BWWSfZCJwfQnAYavwt2z54Ym89707ZBIAVuMytNlQ9ZAbklGZAreWRyxz37fd716bpkB5uhdv2BSi0H5COWZBQHGdvWQZDZD"
f = open("out.json",'w')
f.write(output(fb_id, token))
f.close()
