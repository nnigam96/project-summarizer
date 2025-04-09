import os
from openai import OpenAI

def check_usage():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Get subscription info
    subscription = client.subscriptions.retrieve()
    print("\nSubscription Details:")
    print(f"Plan: {subscription.plan}")
    print(f"Status: {subscription.status}")
    print(f"Rate Limits: {subscription.rate_limit}")
    
    # Get usage for current billing period
    usage = client.usage.retrieve()
    print("\nCurrent Billing Period Usage:")
    print(f"Total Tokens: {usage.total_tokens}")
    print(f"Total Cost: ${usage.total_cost:.2f}")
    
    # Get rate limits
    limits = client.rate_limits.retrieve()
    print("\nRate Limits:")
    print(f"Requests per minute: {limits.requests_per_minute}")
    print(f"Tokens per minute: {limits.tokens_per_minute}")

if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set your OPENAI_API_KEY environment variable")
        print("You can do this by running:")
        print("export OPENAI_API_KEY='your-api-key'")
    else:
        check_usage() 