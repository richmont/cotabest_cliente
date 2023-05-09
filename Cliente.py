import requests
import urllib3
urllib3.disable_warnings()
import json

class Loja():
    def __init__(self, json_dados: dict) -> None:
        """Representa uma loja

        Args:
            json_dados (dict): dicionário com dados da loja

        Raises:
            IndexError: 
            IndexError: 
        """
        self.id_loja = json_dados["id"]
        self.nome = json_dados["name"]
        self.slug = json_dados["slug"]
        self.abertura_especial = json_dados["special_opening"]
        if len(self.abertura_especial) != 0:
            raise IndexError(f"Loja {self.nome} possui abertura especial")

        if len(json_dados["opening_hours"]) > 1:
            self.abre_domingo = True
            for dia in json_dados["opening_hours"]:
                if dia["type"] == "domingo":
                    if dia["opening"] is None:
                        self.abre_domingo = False
                    else:
                        self.horario_abertura_domingo = dia["opening"]
                        self.horario_fechamento_domingo = dia["closure"]
                if dia["type"] == "segunda-a-sabado":
                    self.horario_abertura_semana = dia["opening"]
                    self.horario_fechamento_semana = dia["closure"]

        
        
        

class Cliente():
    def __init__(self, latitude:float = -23.56571961652763, longitude:float = -46.651259360931014) -> None:
        """CLiente da API Cotabest, consulta as lojas do Atacadão

        Args:
            latitude (float, optional): latitude para consulta. Defaults to -23.56571961652763.
            longitude (float, optional): longitude para consulta. Defaults to -46.651259360931014.
        """
        self.lista_lojas = []
        url_api = f"https://apis.cotabest.com.br/folhetos/stores?latitude={latitude}&longitude={longitude}"
        with requests.get(url_api, verify=False) as r:
            self.json_bruto = r.json()
            if r.status_code == 200:
                if r.json()["success"]:
                    self.total_lojas = int(r.json()["total"])
                    self.conteudo_lojas_bruto = r.json()["data"]
        
        #print(self.conteudo_lojas_bruto[0])
        
        for loja_bruto in self.conteudo_lojas_bruto:
            loja = Loja(loja_bruto["store"])
            self.lista_lojas.append(loja)

if __name__ == "__main__":
    try:
        c = Cliente()
        
        for loja in c.lista_lojas:
            if loja.abre_domingo:
                if loja.horario_fechamento_domingo != "18:00:00":
                    print(f"{loja.nome} abre aos domingos as {loja.horario_abertura_domingo} e fecha as {loja.horario_fechamento_domingo}")
            else:
                print(f"{loja.nome} não abre domingo, mas em dia de semana abre as {loja.horario_abertura_semana} e fecha as {loja.horario_fechamento_semana}")
        print("Lojas obtidas no programa: ", len(c.lista_lojas))
    except requests.exceptions.JSONDecodeError:
        print("Falha na requisição, tente novamente")