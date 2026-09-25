# Support Assistant

## Architecture overview

The support assistant follows a standard RAG flow:

1. Ingestion: the documents under `support_assistant/docs` are read and split into short chunks.
2. Embedding: the `SentenceTransformer` model `all-MiniLM-L6-v2` converts each chunk into a vector.
3. Retrieval: ChromaDB stores the vectors in the collection `zepto_policy_collection`; the `retrieve_and_answer` node queries this collection using cosine similarity.
4. Generation: in mock mode, the final answer is the canned template `Based on the retrieved context: ...`; in the optional real-LLM path, the prompt template is built with the role–context–task–format–length skeleton and the answer is validated into the JSON schema.

The routing is handled by the `classify_intent` node using the required keyword heuristic in mock mode, and then a conditional edge routes either to `retrieve_and_answer` or `direct_answer`.

```text
ingestion -> embedding -> retrieval -> generation
   docs/      model + ChromaDB   graph node     mock/real branch
```

The `MOCK_LLM` toggle only affects the generation step. Retrieval still runs for policy questions in both modes; the main change between mock and real-LLM operation is whether the final answer comes from a deterministic template or a model-generated JSON response.

## Mock-mode example calls

Run the service with `MOCK_LLM=1` (the required graded baseline):

```bash
MOCK_LLM=1 uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
```

Then query the app locally:

```bash
curl -X POST http://localhost:7860/ask -H "Content-Type: application/json" -d '{"query": "What is the delivery fee for orders below INR 149?"}'
```

Example response:

```json
{"answer":"Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume.","sources":["doc_01_0"],"confidence":1.0}
```

Another example:

```bash
curl -X POST http://localhost:7860/ask -H "Content-Type: application/json" -d '{"query": "How is the weather today?"}'
```

Example response:

```json
{"answer":"I can only answer questions about Zepto policies right now.","sources":[],"confidence":1.0}
```

## Docker build/run

```bash
cd support_assistant
docker build -t zepto-support-assistant .
docker run -p 7860:7860 zepto-support-assistant
```

The container serves the same `POST /ask` endpoint locally on port `7860`.

## Notes

This is a grounded, no-cost, offline baseline: no LLM provider keys or paid subscriptions are required. The mock branch is what is graded. The optional real-LLM extension is present in code but remains inactive when `MOCK_LLM` is left at its default value.
