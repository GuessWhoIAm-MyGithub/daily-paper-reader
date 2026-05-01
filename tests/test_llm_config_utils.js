const assert = require('node:assert/strict');

const {
  normalizeBaseUrlForStorage,
  buildRequestEndpoint,
  buildChatCompletionsEndpoint,
  sanitizeModelList,
  migrateLegacySecret,
  resolveLLMConfig,
  resolveChatModels,
  resolveSummaryLLM,
  inferProviderType,
  getOpenAICompatiblePreset,
  inferChatApiProfile,
  shouldUseXApiKeyHeader,
  buildStreamingChatPayload,
  buildConnectivityTestPayload,
  buildChatRequest,
  extractChatResponseText,
} = require('../app/llm-config-utils.js');

function testNormalizeBaseUrlForStorage() {
  assert.equal(
    normalizeBaseUrlForStorage('https://api.example.com/v1/chat/completions'),
    'https://api.example.com/v1',
  );
  assert.equal(
    normalizeBaseUrlForStorage('https://api.anthropic.com/v1/messages'),
    'https://api.anthropic.com/v1',
  );
}

function testBuildRequestEndpoint() {
  assert.equal(
    buildChatCompletionsEndpoint('https://api.example.com/v1'),
    'https://api.example.com/v1/chat/completions',
  );
  assert.equal(
    buildRequestEndpoint('https://api.anthropic.com/v1', 'anthropic'),
    'https://api.anthropic.com/v1/messages',
  );
}

function testSanitizeModelList() {
  assert.deepEqual(
    sanitizeModelList(['gpt-4o', ' gpt-4o ', 'qwen-max', 'glm-4.5', 'extra'], 3),
    ['gpt-4o', 'qwen-max', 'glm-4.5'],
  );
}

function testResolveUnifiedSecret() {
  const secret = {
    llm: {
      request_format: 'openai',
      base_url: 'https://api.example.com/v1',
      api_key: 'sk-unified',
      models: {
        chat: ['gpt-4.1-mini', 'claude-sonnet-4'],
        enrich: 'gpt-4.1-mini',
        refine: 'gpt-4.1-mini',
        summary: 'gpt-4.1',
        rerank: 'gpt-4.1-mini',
      },
    },
  };

  const llm = resolveLLMConfig(secret);
  assert.equal(llm.requestFormat, 'openai');
  assert.equal(llm.models.summary, 'gpt-4.1');

  const chatModels = resolveChatModels(secret);
  assert.equal(chatModels.length, 2);
  assert.equal(chatModels[0].requestFormat, 'openai');

  const summary = resolveSummaryLLM(secret);
  assert.equal(summary.model, 'gpt-4.1');
}

function testMigrateLegacySecret() {
  const migrated = migrateLegacySecret({
    summarizedLLM: {
      apiKey: 'sk-summary',
      baseUrl: 'https://api.bltcy.ai/v1',
      model: 'gpt-5-chat',
    },
    rerankerLLM: {
      apiKey: 'sk-summary',
      baseUrl: 'https://api.bltcy.ai/v1',
      model: 'qwen3-reranker-4b',
    },
    chatLLMs: [
      {
        apiKey: 'sk-chat',
        baseUrl: 'https://api.bltcy.ai/v1',
        models: ['gpt-5-chat', 'deepseek-v3.2'],
      },
    ],
  });

  assert.equal(migrated.llm.request_format, 'openai');
  assert.equal(migrated.llm.base_url, 'https://api.bltcy.ai/v1');
  assert.deepEqual(migrated.llm.models.chat, ['gpt-5-chat', 'deepseek-v3.2']);
  assert.equal(migrated.llm.models.rerank, 'qwen3-reranker-4b');
}

function testInferProviderType() {
  assert.equal(
    inferProviderType({
      llm: {
        request_format: 'anthropic',
        base_url: 'https://api.anthropic.com/v1',
        api_key: 'sk',
        models: { chat: ['claude-sonnet-4'], summary: 'claude-sonnet-4' },
      },
    }),
    'anthropic',
  );
  assert.equal(
    inferProviderType({
      llm: {
        request_format: 'openai',
        base_url: 'https://api.openai.com/v1',
        api_key: 'sk',
        models: { chat: ['gpt-4.1-mini'], summary: 'gpt-4.1-mini' },
      },
    }),
    'openai-compatible',
  );
}

function testGetPreset() {
  assert.deepEqual(
    getOpenAICompatiblePreset('anthropic'),
    {
      key: 'anthropic',
      label: 'Anthropic 官方',
      requestFormat: 'anthropic',
      baseUrl: 'https://api.anthropic.com/v1',
      models: ['claude-sonnet-4-20250514', 'claude-3-7-sonnet-latest'],
    },
  );
}

function testInferChatApiProfile() {
  assert.equal(
    inferChatApiProfile('https://api.deepseek.com', 'deepseek-chat'),
    'deepseek',
  );
  assert.equal(
    inferChatApiProfile('https://api.anthropic.com/v1', 'claude-sonnet-4-20250514'),
    'anthropic',
  );
  assert.equal(
    inferChatApiProfile('https://api.openai.com/v1', 'gpt-4.1-mini'),
    'generic-openai',
  );
}

function testShouldUseXApiKeyHeader() {
  assert.equal(
    shouldUseXApiKeyHeader({
      baseUrl: 'https://api.minimaxi.com/v1',
      model: 'MiniMax-M2.5',
    }),
    false,
  );
  assert.equal(
    shouldUseXApiKeyHeader({
      baseUrl: 'https://api.openai.com/v1',
      model: 'gpt-4.1-mini',
    }),
    true,
  );
}

function testBuildStreamingChatPayload() {
  assert.deepEqual(
    buildStreamingChatPayload({
      requestFormat: 'openai',
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-reasoner',
      messages: [{ role: 'user', content: 'hi' }],
    }),
    {
      model: 'deepseek-reasoner',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
      thinking: { type: 'enabled' },
    },
  );

  assert.deepEqual(
    buildStreamingChatPayload({
      requestFormat: 'anthropic',
      baseUrl: 'https://api.anthropic.com/v1',
      model: 'claude-sonnet-4-20250514',
      messages: [
        { role: 'system', content: 'Only answer briefly.' },
        { role: 'user', content: 'hi' },
      ],
    }),
    {
      model: 'claude-sonnet-4-20250514',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
      max_tokens: 4096,
      system: 'Only answer briefly.',
    },
  );
}

function testBuildConnectivityTestPayload() {
  assert.deepEqual(
    buildConnectivityTestPayload({
      requestFormat: 'anthropic',
      baseUrl: 'https://api.anthropic.com/v1',
      model: 'claude-sonnet-4-20250514',
    }),
    {
      model: 'claude-sonnet-4-20250514',
      system: 'Reply with exactly: hello world',
      messages: [
        { role: 'user', content: 'hello world' },
      ],
      temperature: 0,
      max_tokens: 256,
    },
  );
}

function testBuildChatRequest() {
  const openaiRequest = buildChatRequest({
    requestFormat: 'openai',
    baseUrl: 'https://api.openai.com/v1',
    apiKey: 'sk-openai',
    model: 'gpt-4.1-mini',
    messages: [{ role: 'user', content: 'hi' }],
    stream: false,
    temperature: 0,
    maxTokens: 256,
    responseFormat: { type: 'json_object' },
  });
  assert.equal(openaiRequest.endpoint, 'https://api.openai.com/v1/chat/completions');
  assert.equal(openaiRequest.headers.Authorization, 'Bearer sk-openai');
  assert.equal(openaiRequest.body.response_format.type, 'json_object');

  const anthropicRequest = buildChatRequest({
    requestFormat: 'anthropic',
    baseUrl: 'https://api.anthropic.com/v1',
    apiKey: 'sk-anthropic',
    model: 'claude-sonnet-4-20250514',
    messages: [
      { role: 'system', content: 'Only JSON.' },
      { role: 'user', content: 'hi' },
    ],
    stream: false,
    temperature: 0,
    maxTokens: 256,
    responseFormat: { type: 'json_object' },
  });
  assert.equal(anthropicRequest.endpoint, 'https://api.anthropic.com/v1/messages');
  assert.equal(anthropicRequest.headers['x-api-key'], 'sk-anthropic');
  assert.equal(anthropicRequest.body.system.includes('Only JSON.'), true);
}

function testExtractChatResponseText() {
  assert.equal(
    extractChatResponseText(
      {
        choices: [{ message: { content: 'hello openai' } }],
      },
      'openai',
    ),
    'hello openai',
  );
  assert.equal(
    extractChatResponseText(
      {
        content: [{ type: 'text', text: 'hello anthropic' }],
      },
      'anthropic',
    ),
    'hello anthropic',
  );
}

testNormalizeBaseUrlForStorage();
testBuildRequestEndpoint();
testSanitizeModelList();
testResolveUnifiedSecret();
testMigrateLegacySecret();
testInferProviderType();
testGetPreset();
testInferChatApiProfile();
testShouldUseXApiKeyHeader();
testBuildStreamingChatPayload();
testBuildConnectivityTestPayload();
testBuildChatRequest();
testExtractChatResponseText();

console.log('llm config utils tests passed');
