import asyncio
import httpx
import sys

async def main():
    base_url = "http://127.0.0.1:8000/api/v1"
    print("Testing connection to backend server...", flush=True)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Health check
        try:
            r = await client.get(f"{base_url}/health")
            print(f"1. Health Check [{r.status_code}]:", r.json(), flush=True)
            assert r.status_code == 200
        except Exception as e:
            print("ERROR connecting to health check:", e, flush=True)
            return False

        # 2. Products query (the one in user's error message)
        try:
            r = await client.get(f"{base_url}/products?sort_by=price_asc&page_size=20")
            print(f"2. Products Query [{r.status_code}]:", f"Found {len(r.json())} products", flush=True)
            assert r.status_code == 200
            assert len(r.json()) > 0
        except Exception as e:
            print("ERROR connecting to products endpoint:", e, flush=True)
            return False

        # 3. AI Assistant Chat query (the one in user's error message)
        try:
            print("3. Testing AI Assistant Chat with live Gemini model...", flush=True)
            r = await client.post(
                f"{base_url}/assistant/chat",
                json={"message": "I want a flagship phone under ₹80,000 with best camera"}
            )
            print(f"   AI Assistant [{r.status_code}]:", flush=True)
            data = r.json()
            print(f"   Model used: {data.get('model_used')}", flush=True)
            print(f"   AI Message: {data.get('message')[:120]}...", flush=True)
            print(f"   Recommended products count: {len(data.get('recommended_products', []))}", flush=True)
            assert r.status_code == 200
            assert len(data.get("message", "")) > 0
        except Exception as e:
            print("ERROR in AI assistant endpoint:", e, flush=True)
            return False

        print("\nALL LIVE SERVER TESTS PASSED SUCCESSFULLY!", flush=True)
        return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
