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
  "config_url": "[https://seu-app-no-render.com/config](https://seu-app-no-render.com/config)",
  "json_params_url": "[https://seu-app-no-render.com/json-params](https://seu-app-no-render.com/json-params)",
  "user_url": "[https://seu-app-no-render.com/deploy](https://seu-app-no-render.com/deploy)",
  "analytics_url": "[https://seu-app-no-render.com/analytics-data](https://seu-app-no-render.com/analytics-data)",
  "analytics_list_url": "[https://seu-app-no-render.com/analytics-list](https://seu-app-no-render.com/analytics-list)"
}