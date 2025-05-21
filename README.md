# NUVYOLO - API de Detecção de Objetos

API para detecção e rastreamento de objetos em streams de vídeo utilizando YOLO.

## Estrutura do Projeto

```
app/
├── __init__.py
├── main.py                 
├── config/                 # Configurações da aplicação
├── api/                    # Definições da API
│   ├── models/             # Modelos Pydantic
│   ├── routes/             # Endpoints da API
├── core/                   # Lógica de negócio
├── external/               # Integração com APIs externas
├── utils/                  # Funções utilitárias
```

## Requisitos

- Python 3.10+
- OpenCV
- FastAPI
- YOLO (Ultralytics)
- sshpass
- nvidia-container-toolkit
- Outros requisitos em `requirements.txt`

## Configuração

1. Clonar o repositório:
   ```bash
   git clone <repositório>
   cd nuvyolo
   ```

2. Criar um ambiente virtual e instalar as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar as variáveis de ambiente (`.env`)

4. Baixe os modelos YOLO (YOLOv8) (Opcinal, YOLO baixa durante a execução)`:
   ```bash
   # Baixe os modelos manualmente ou use o script:
   # python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

## Executando a Aplicação

### Desenvolvimento

```bash
uvicorn app.main:app --reload
```

### Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Com Docker

```bash
docker-compose up -d
```

## API Endpoints

- `GET /`: Informações sobre a API
- `POST /monitor`: Iniciar monitoramento em uma câmera
- `POST /stop/{camera_id}`: Parar monitoramento em uma câmera
- `POST /stop/all`: Parar monitoramento em todas as câmeras
- `GET /monitored`: Listar câmeras monitoradas

## Exemplo de Uso

### Iniciar Monitoramento

```bash
curl -X POST "http://localhost:8000/monitor" \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": 51
    "device": "cpu",
    "detection_model_path": "models/yolov8n.pt",
    "classes": ["person", "car", "truck"],
    "tracker_model": "bytetrack.yaml",
    "frames_per_second": 5,
    "frames_before_disappearance": 30,
    "confidence_threshold": 0.25,
    "iou": 0.45
  }'
```

### Parar Monitoramento

```bash
curl -X POST "http://localhost:8000/stop/1"
```

### Verificar Câmeras Monitoradas

```bash
curl "http://localhost:8000/monitored"
```

## Documentação da API

A documentação automática da API está disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
