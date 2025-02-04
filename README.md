# LLM Chatbot App ⚡

#### Frontend Original Link
[Github](https://github.com/a16z-infra/llama2-chatbot)


<img width="1710" alt="llama2 demo" src="https://github.com/a16z-infra/llama2-chatbot/assets/5958899/7512cbd3-ef90-4a9f-b9f6-eab5be7a483f">

## Features

- Chat history is maintained for each session (if you refresh, chat history clears)
- Intergration with Ollama
- Use Open Models on Local Environment

## Installation

- Clone the repository
```
git clone https://github.com/mnc1423/llm_app.git
```
- Install Ollama (Docker or local Installation) [Ollama Github](https://github.com/ollama/ollama)


- Get Ollama Models [Ollama Models](https://ollama.com/search)
```
ollama pull deepseek-r1
```

- Run App
```
docker compose up -d 
OR streamlit run --server.port 8501 --server.address 0.0.0.0 Default_Chat.py
```



## Usage

- General Chat (with Prompts)
- RAG based Chat (Currently Under Development)
- Customized Local Vector DB [Exmaple Vector DB API](https://github.com/mnc1423/chroma_api) 
- Image Processing



## Using HF Models (safetensors -> hhuf-> ollama)
- Clone HF repo (with safetensors Inside)
- Using llama.cpp [Github](https://github.com/ggerganov/llama.cpp)
```
python llama.cpp/convert_hf_to_gguf.py <repo_path> --outfile <model>.gguf --outtype <type>
```
- Using Ollama
```
echo "FROM <created Model>" > Modelfile
ollama create <ollama Model> -f Modelfile
```

## TODO
- Add endpoints for Non open Models (OpenAI, Gemini, etc)
- Hungging Face model integration 
- Vectorize data other than PDF