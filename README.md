\# ReceiptWise — Order \& Warranty Agent



ReceiptWise is a proactive post-purchase assistant that reads a shopper’s receipt or order confirmation and immediately shows purchased items, return deadlines, warranty coverage, and expiring-soon alerts before the shopper asks a question.



\## Key features



\- Automatic return and warranty calculation immediately after receipt upload

\- Expiring-soon Return Radar for windows with fewer than 7 days left

\- Receipt-aware RAG using Chroma and Ollama embeddings

\- Grounded answers with visible receipt and store-policy sources

\- Live mock order-status lookup by order ID

\- Safe handling for missing orders and invalid receipts

\- Multi-step agent flow: retrieval plus live order-status lookup in one query



\## Tech stack



\- Python

\- Streamlit

\- LangChain

\- ChatOllama using Llama 3.2

\- Ollama `nomic-embed-text` embeddings

\- Chroma vector database

\- SQLite mock order database



\## Setup



```bash

pip install -r requirements.txt

ollama pull llama3.2

ollama pull nomic-embed-text

python seed-data.py

```



\## Run locally



```bash

streamlit run app.py

```



Open `http://localhost:8501` in a browser.



\## Demo flow



1\. Upload `data/sample-receipt.txt`.

2\. Show the automatic Alpine Winter Jacket expiry warning.

3\. Ask: `When can I return the jacket?`

4\. Check order ID: `ORD-1001`.

5\. Ask: `Can I return the jacket, and what is the status of ORD-1001?`

6\. Check safe failure with: `ORD-9999`.



\## Deliberate design decision



ReceiptWise runs deterministic deadline calculations at upload time, rather than waiting for a user question. This makes expiring return windows visible before shoppers lose the opportunity to act.# ReceiptWise — Order \& Warranty Agent



ReceiptWise is a proactive post-purchase assistant that reads a shopper’s receipt or order confirmation and immediately shows purchased items, return deadlines, warranty coverage, and expiring-soon alerts before the shopper asks a question.



\## Key features



\- Automatic return and warranty calculation immediately after receipt upload

\- Expiring-soon Return Radar for windows with fewer than 7 days left

\- Receipt-aware RAG using Chroma and Ollama embeddings

\- Grounded answers with visible receipt and store-policy sources

\- Live mock order-status lookup by order ID

\- Safe handling for missing orders and invalid receipts

\- Multi-step agent flow: retrieval plus live order-status lookup in one query



\## Tech stack



\- Python

\- Streamlit

\- LangChain

\- ChatOllama using Llama 3.2

\- Ollama `nomic-embed-text` embeddings

\- Chroma vector database

\- SQLite mock order database



\## Setup



```bash

pip install -r requirements.txt

ollama pull llama3.2

ollama pull nomic-embed-text

python seed-data.py

```



\## Run locally



```bash

streamlit run app.py

```



Open `http://localhost:8501` in a browser.



\## Demo flow



1\. Upload `data/sample-receipt.txt`.

2\. Show the automatic Alpine Winter Jacket expiry warning.

3\. Ask: `When can I return the jacket?`

4\. Check order ID: `ORD-1001`.

5\. Ask: `Can I return the jacket, and what is the status of ORD-1001?`

6\. Check safe failure with: `ORD-9999`.



\## Deliberate design decision



ReceiptWise runs deterministic deadline calculations at upload time, rather than waiting for a user question. This makes expiring return windows visible before shoppers lose the opportunity to act.# ReceiptWise — Order \& Warranty Agent



ReceiptWise is a proactive post-purchase assistant that reads a shopper’s receipt or order confirmation and immediately shows purchased items, return deadlines, warranty coverage, and expiring-soon alerts before the shopper asks a question.



\## Key features



\- Automatic return and warranty calculation immediately after receipt upload

\- Expiring-soon Return Radar for windows with fewer than 7 days left

\- Receipt-aware RAG using Chroma and Ollama embeddings

\- Grounded answers with visible receipt and store-policy sources

\- Live mock order-status lookup by order ID

\- Safe handling for missing orders and invalid receipts

\- Multi-step agent flow: retrieval plus live order-status lookup in one query



\## Tech stack



\- Python

\- Streamlit

\- LangChain

\- ChatOllama using Llama 3.2

\- Ollama `nomic-embed-text` embeddings

\- Chroma vector database

\- SQLite mock order database



\## Setup



```bash

pip install -r requirements.txt

ollama pull llama3.2

ollama pull nomic-embed-text

python seed-data.py

```



\## Run locally



```bash

streamlit run app.py

```



Open `http://localhost:8501` in a browser.



\## Demo flow



1\. Upload `data/sample-receipt.txt`.

2\. Show the automatic Alpine Winter Jacket expiry warning.

3\. Ask: `When can I return the jacket?`

4\. Check order ID: `ORD-1001`.

5\. Ask: `Can I return the jacket, and what is the status of ORD-1001?`

6\. Check safe failure with: `ORD-9999`.



\## Deliberate design decision



ReceiptWise runs deterministic deadline calculations at upload time, rather than waiting for a user question. This makes expiring return windows visible before shoppers lose the opportunity to act.# ReceiptWise — Order \& Warranty Agent



ReceiptWise is a proactive post-purchase assistant that reads a shopper’s receipt or order confirmation and immediately shows purchased items, return deadlines, warranty coverage, and expiring-soon alerts before the shopper asks a question.



\## Key features



\- Automatic return and warranty calculation immediately after receipt upload

\- Expiring-soon Return Radar for windows with fewer than 7 days left

\- Receipt-aware RAG using Chroma and Ollama embeddings

\- Grounded answers with visible receipt and store-policy sources

\- Live mock order-status lookup by order ID

\- Safe handling for missing orders and invalid receipts

\- Multi-step agent flow: retrieval plus live order-status lookup in one query



\## Tech stack



\- Python

\- Streamlit

\- LangChain

\- ChatOllama using Llama 3.2

\- Ollama `nomic-embed-text` embeddings

\- Chroma vector database

\- SQLite mock order database



\## Setup



```bash

pip install -r requirements.txt

ollama pull llama3.2

ollama pull nomic-embed-text

python seed-data.py

```



\## Run locally



```bash

streamlit run app.py

```



Open `http://localhost:8501` in a browser.



\## Demo flow



1\. Upload `data/sample-receipt.txt`.

2\. Show the automatic Alpine Winter Jacket expiry warning.

3\. Ask: `When can I return the jacket?`

4\. Check order ID: `ORD-1001`.

5\. Ask: `Can I return the jacket, and what is the status of ORD-1001?`

6\. Check safe failure with: `ORD-9999`.



\## Deliberate design decision



ReceiptWise runs deterministic deadline calculations at upload time, rather than waiting for a user question. This makes expiring return windows visible before shoppers lose the opportunity to act.# ReceiptWise — Order \& Warranty Agent



ReceiptWise is a proactive post-purchase assistant that reads a shopper’s receipt or order confirmation and immediately shows purchased items, return deadlines, warranty coverage, and expiring-soon alerts before the shopper asks a question.



\## Key features



\- Automatic return and warranty calculation immediately after receipt upload

\- Expiring-soon Return Radar for windows with fewer than 7 days left

\- Receipt-aware RAG using Chroma and Ollama embeddings

\- Grounded answers with visible receipt and store-policy sources

\- Live mock order-status lookup by order ID

\- Safe handling for missing orders and invalid receipts

\- Multi-step agent flow: retrieval plus live order-status lookup in one query



\## Tech stack



\- Python

\- Streamlit

\- LangChain

\- ChatOllama using Llama 3.2

\- Ollama `nomic-embed-text` embeddings

\- Chroma vector database

\- SQLite mock order database



\## Setup



```bash

pip install -r requirements.txt

ollama pull llama3.2

ollama pull nomic-embed-text

python seed-data.py

```



\## Run locally



```bash

streamlit run app.py

```



Open `http://localhost:8501` in a browser.



\## Demo flow



1\. Upload `data/sample-receipt.txt`.

2\. Show the automatic Alpine Winter Jacket expiry warning.

3\. Ask: `When can I return the jacket?`

4\. Check order ID: `ORD-1001`.

5\. Ask: `Can I return the jacket, and what is the status of ORD-1001?`

6\. Check safe failure with: `ORD-9999`.



\## Deliberate design decision



ReceiptWise runs deterministic deadline calculations at upload time, rather than waiting for a user question. This makes expiring return windows visible before shoppers lose the opportunity to act.v

