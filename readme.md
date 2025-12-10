## 🔌 Registo na Inven!RA

Para registar este Activity Provider na plataforma, utilize os seguintes endpoints (definidos no ficheiro `invenra_register.json`):

| Serviço | Método | Endpoint |
| :--- | :---: | :--- |
| **Configuração** | `GET` | `/config` |
| **Parâmetros** | `GET` | `/json-params` |
| **Deploy** | `GET` | `/deploy` |
| **Lista de Analytics** | `GET` | `/analytics-list` |
| **Dados de Analytics** | `POST` | `/analytics-data` |

### 📄 JSON de Registo Completo

Copie o conteúdo abaixo para registar a atividade:

```json
{
  "name": "WordMemorizer Game",
  "config_url": "https://wordmemorizer.onrender.com/config",
  "json_params_url": "https://wordmemorizer.onrender.com/json-params",
  "user_url": "https://wordmemorizer.onrender.com/deploy",
  "analytics_url": "https://wordmemorizer.onrender.com/analytics-data",
  "analytics_list_url": "https://wordmemorizer.onrender.com/analytics-list"
}