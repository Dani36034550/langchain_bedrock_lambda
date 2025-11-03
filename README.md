🚀 Enterprise RAG Lambda
LangChain + AWS Bedrock + Pinecone (Serverless Microservice with SAM, Docker & Secrets Manager)

This project implements a production-grade Retrieval-Augmented Generation (RAG) microservice using:

✅ LangChain
✅ Amazon Bedrock (Titan embeddings + LLM)
✅ Pinecone Vector Database
✅ AWS Lambda (Docker)
✅ AWS SAM deployment
✅ Secrets Manager for secure API key storage
✅ Amazon ECR for container images

Designed to showcase enterprise GenAI engineering expertise, combining secure serverless architecture + scalable vector search + LLM pipeline.

🧠 Key Features
Category	Details
AI Model	Amazon Bedrock (Titan) via LangChain
Vector DB	Pinecone Serverless
Deployment	AWS SAM + Docker → ECR → Lambda
Secrets	Pinecone API key stored in AWS Secrets Manager
API	REST endpoint via Amazon API Gateway
Use Case	RAG: retrieve relevant chunks & generate answer
Documents	PDF/Text ingestion script included
🧩 Architecture
Client → API Gateway → Lambda (Docker)
       ↓                 ↓
   Secrets Manager     LangChain RAG
                             ↓
             Pinecone Vector Search + Amazon Bedrock

📦 Local Setup
1️⃣ Create Virtual Env
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

2️⃣ Install Requirements
pip install -r requirements.txt

🔐 Store Pinecone Key in AWS Secrets Manager
aws secretsmanager create-secret \
  --name pinecone/api \
  --secret-string "{\"PINECONE_API_KEY\":\"YOUR_KEY_HERE\"}"

🧠 Ingest Documents (PDFs → Pinecone)

Place your data in ./data/

Run ingestion:

python ingest_documents.py


This performs:

PDF parsing

Text chunking (LangChain)

Titan embeddings

Vector upsert to Pinecone

🐳 Build & Deploy to AWS
1️⃣ Build image + Lambda using SAM
sam build

2️⃣ Deploy (Guided first time)
sam deploy --guided


Will provision:

ECR repo

Lambda function

API Gateway endpoint

IAM roles

Secret access permissions

🌐 Invoke the API

Using curl:

curl -X POST \
"https://<your-api-id>.execute-api.<region>.amazonaws.com/Prod/query" \
-H "Content-Type: application/json" \
-d '{"query":"What is Amazon Bedrock?"}'

📁 Project Structure
.
├── lambda_handler.py
├── chain_builder.py
├── ingest_documents.py
├── requirements.txt
├── Dockerfile
├── template.yaml           # AWS SAM Template
└── data/                   # PDFs or text files to ingest

🏢 Enterprise-Grade Highlights

✅ Secure secret management (no keys in Lambda)
✅ Serverless architecture & autoscaling
✅ Bedrock for enterprise LLM access control
✅ Pinecone for vector search at scale
✅ Infrastructure as Code via SAM
✅ Docker-based Lambda = portable, production-ready

🚀 Use this repo to showcase:

GenAI engineering

AWS serverless mastery

Enterprise deployment patterns

RAG expertise (Bedrock + LangChain + Pinecone)