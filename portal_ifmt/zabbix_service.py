import requests
import json

class ZabbixAPI:
    def __init__(self):
        self.url = "http://10.1.140.70/api_jsonrpc.php" 
        self.user = ""
        self.password = ""
        self.auth_token = None
        self.headers = {'Content-Type': 'application/json-rpc'}

    def _call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        if self.auth_token:
            payload["auth"] = self.auth_token
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return response.json().get('result')

    def login(self):
        result = self._call("user.login", {"username": self.user, "password": self.password})
        if result:
            self.auth_token = result
        return self.auth_token

    def _fetch_history(self, itemid, limite, value_type=0):
        if not itemid: 
            return [0] * limite
        
        history = self._call("history.get", {
            "output": "extend",
            "history": value_type,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": limite
        })
        
        if not history: 
            return [0] * limite
            
        valores = [round(float(h['value']), 3) for h in history]
        while len(valores) < limite:
            valores.append(0)
            
        return valores[::-1]

    def get_vm_metrics_full(self, vm_name, limite_historico=10):
        if not self.auth_token:
            self.login()

        hosts = self._call("host.get", {
            "filter": {"host": [vm_name]},
            "output": ["hostid"]
        })

        if not hosts:
            return {"erro": "Máquina não encontrada no Zabbix"}
        
        host_id = hosts[0]['hostid']

        items = self._call("item.get", {
            "hostids": host_id,
            "output": ["itemid", "name", "key_", "lastvalue"]
        })

        ids = {}
        last_values = {}

        def safe_float(valor_str):
            try:
                return float(valor_str) if valor_str else 0.0
            except ValueError:
                return 0.0

        for item in items:
            nome = item['name']
            chave = item['key_']
            raw_value = item['lastvalue']

            if "system.cpu.util" in chave or "CPU utilization" in nome:
                ids["cpu"] = item['itemid']
            
            elif "Memory utilization" in nome or "vm.memory.util" in chave:
                ids["ram"] = item['itemid']
            
            elif ("/: Total space" in nome) or ("vfs.fs.size" in chave and "total" in chave and "boot" not in chave):
                last_values["disco_total"] = safe_float(raw_value)
                
            elif ("/: Used space" in nome) or ("vfs.fs.size" in chave and "used" in chave and "boot" not in chave):
                last_values["disco_used"] = safe_float(raw_value)
                
            elif "Bits received" in nome and "ens3" in nome:
                ids["net_in"] = item['itemid']
                
            elif "Bits sent" in nome and "ens3" in nome:
                ids["net_out"] = item['itemid']

        history_data = {
            "cpu_hist": self._fetch_history(ids.get("cpu"), limite_historico, 0),
            "ram_hist": self._fetch_history(ids.get("ram"), limite_historico, 0),
            "net_in_hist": [round(b / 1000000, 3) for b in self._fetch_history(ids.get("net_in"), limite_historico, 3)],
            "net_out_hist": [round(b / 1000000, 3) for b in self._fetch_history(ids.get("net_out"), limite_historico, 3)]
        }

        total_disco_raw = last_values.get("disco_total", 1) 
        used_disco_raw = last_values.get("disco_used", 0)
        
        total_disco_gb = round(total_disco_raw / (1024**3), 2)
        used_disco_gb = round(used_disco_raw / (1024**3), 2)
        free_disco_gb = round((total_disco_raw - used_disco_raw) / (1024**3), 2)

        return {
            "historico": {
                "labels": [""] * limite_historico,
                "cpu": history_data["cpu_hist"],
                "ram": history_data["ram_hist"],
                "net_in": history_data["net_in_hist"],
                "net_out": history_data["net_out_hist"],
            },
            "pizza_disco": {
                "labels": ["Usado (GB)", "Livre (GB)"],
                "data": [used_disco_gb, free_disco_gb],
                "total_gb": total_disco_gb
            }
        }