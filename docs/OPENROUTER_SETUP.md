# OpenRouter Configuration Guide

## What is OpenRouter?

OpenRouter is an API aggregator that provides access to multiple LLM providers (OpenAI, Anthropic, Google, Meta, etc.) through a single unified API. This is **ideal for production use** because:

1. **Flexibility**: Switch between models without code changes
2. **Cost Optimization**: Choose the best price/performance ratio
3. **Fallback Support**: Automatically fallback to alternative models
4. **One API Key**: Access 100+ models with one key

## Setup

### 1. Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up for an account
3. Go to https://openrouter.ai/keys
4. Create a new API key
5. Add credits to your account

### 2. Configure .env

```env
# OpenRouter configuration
OPENAI_API_KEY=sk-or-v1-your-openrouter-key-here
DEFAULT_LLM=openrouter
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
```

**Note**: OpenRouter uses `OPENAI_API_KEY` because it's OpenAI-compatible!

### 3. Choose Your Model

OpenRouter supports 100+ models. Popular choices:

**Best for Quality:**
- `anthropic/claude-3.5-sonnet` - Highly recommended
- `openai/gpt-4-turbo`
- `google/gemini-pro-1.5`

**Best for Cost:**
- `anthropic/claude-3-haiku`
- `openai/gpt-3.5-turbo`
- `meta-llama/llama-3.1-70b-instruct`

**Best for Speed:**
- `anthropic/claude-3-haiku`
- `google/gemini-flash-1.5`

See full model list: https://openrouter.ai/models

## Pricing

OpenRouter charges per-token with no markup. Example costs:

- **Claude 3.5 Sonnet**: $3/M input, $15/M output tokens
- **GPT-4 Turbo**: $10/M input, $30/M output tokens
- **Claude 3 Haiku**: $0.25/M input, $1.25/M output tokens

Check current pricing: https://openrouter.ai/models

## Model Recommendations for Newsletter Manager

### Development/Testing
```env
DEFAULT_MODEL=anthropic/claude-3-haiku
```
Fast and cheap for testing ($0.25/M input)

### Production
```env
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
```
Best quality for content generation and user interactions

### Budget Production
```env
DEFAULT_MODEL=openai/gpt-3.5-turbo
```
Good balance of cost and quality

## Switching Models

You can switch models anytime by changing `.env`:

```env
# Before
DEFAULT_MODEL=anthropic/claude-3-haiku

# After (no code changes needed!)
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
```

Restart the application to apply changes.

## Testing

```bash
# Test OpenRouter connection
python -c "from src.config.llm import get_llm; llm = get_llm(); print('✅ OpenRouter connected!')"
```

## Fallback Strategy

For production, you can implement fallback logic:

```python
# Try primary model
DEFAULT_MODEL=anthropic/claude-3.5-sonnet

# If it fails, the application will show an error
# You can manually switch to:
# DEFAULT_MODEL=anthropic/claude-3-haiku
```

Future enhancement: Automatic model fallback in code.

## Benefits for This Project

1. **Flexibility**: Switch between Claude, GPT-4, Gemini as needed
2. **Cost Control**: Start with cheap models, upgrade for production
3. **No Vendor Lock-in**: Not tied to one provider
4. **Easy Testing**: Test with different models to find best fit
5. **One Bill**: All LLM costs in one place

---

**Ready to use!** Just set your OpenRouter API key in `.env` and you're good to go! 🚀
