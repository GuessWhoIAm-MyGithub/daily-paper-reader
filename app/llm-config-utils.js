(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.DPRLLMConfigUtils = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const DEFAULT_REQUEST_FORMAT = 'openai';
  const DEFAULT_ANTHROPIC_VERSION = '2023-06-01';

  const OPENAI_COMPATIBLE_PRESETS = Object.freeze({
    deepseek: Object.freeze({
      key: 'deepseek',
      label: 'DeepSeek 官方',
      requestFormat: 'openai',
      baseUrl: 'https://api.deepseek.com',
      models: Object.freeze(['deepseek-chat', 'deepseek-reasoner']),
    }),
    glm: Object.freeze({
      key: 'glm',
      label: 'GLM Coding Plan',
      requestFormat: 'openai',
      baseUrl: 'https://open.bigmodel.cn/api/coding/paas/v4',
      models: Object.freeze(['GLM-4.7', 'GLM-5', 'GLM-4.6']),
    }),
    minimax: Object.freeze({
      key: 'minimax',
      label: 'MiniMax Coding Plan',
      requestFormat: 'openai',
      baseUrl: 'https://api.minimaxi.com/v1',
      models: Object.freeze(['MiniMax-M2.5', 'MiniMax-M2.7', 'MiniMax-M2.1']),
    }),
    kimi: Object.freeze({
      key: 'kimi',
      label: 'Kimi 编程预设',
      requestFormat: 'openai',
      baseUrl: 'https://api.moonshot.ai/v1',
      models: Object.freeze(['kimi-k2.5', 'kimi-k2-turbo-preview', 'kimi-k2-thinking']),
    }),
    openai: Object.freeze({
      key: 'openai',
      label: 'OpenAI 官方',
      requestFormat: 'openai',
      baseUrl: 'https://api.openai.com/v1',
      models: Object.freeze(['gpt-4.1-mini', 'gpt-4.1']),
    }),
    anthropic: Object.freeze({
      key: 'anthropic',
      label: 'Anthropic 官方',
      requestFormat: 'anthropic',
      baseUrl: 'https://api.anthropic.com/v1',
      models: Object.freeze(['claude-sonnet-4-20250514', 'claude-3-7-sonnet-latest']),
    }),
  });

  const normalizeText = (value) => String(value || '').trim();

  const normalizeRequestFormat = (value) => {
    const lowered = normalizeText(value).toLowerCase();
    if (lowered === 'anthropic' || lowered === 'claude') return 'anthropic';
    return 'openai';
  };

  const inferRequestFormatFromBaseUrl = (baseUrl) => {
    const normalized = normalizeText(baseUrl).toLowerCase();
    if (/anthropic\.com/.test(normalized)) return 'anthropic';
    return 'openai';
  };

  const normalizeBaseUrlForStorage = (value) => {
    let text = normalizeText(value).replace(/\/+$/g, '');
    if (!text) return '';
    text = text.replace(/\/chat\/completions$/i, '');
    text = text.replace(/\/messages$/i, '');
    return text.replace(/\/+$/g, '');
  };

  const buildRequestEndpoint = (value, requestFormat) => {
    const raw = normalizeText(value).replace(/\/+$/g, '');
    if (!raw) return '';
    const format = normalizeRequestFormat(requestFormat || inferRequestFormatFromBaseUrl(raw));
    if (format === 'anthropic') {
      if (/\/messages$/i.test(raw)) return raw;
      const normalized = normalizeBaseUrlForStorage(raw);
      if (!normalized) return '';
      if (/\/v\d+$/i.test(normalized)) {
        return `${normalized}/messages`;
      }
      return `${normalized}/v1/messages`;
    }
    if (/\/chat\/completions$/i.test(raw)) return raw;
    const normalized = normalizeBaseUrlForStorage(raw);
    if (!normalized) return '';
    if (/\/v\d+$/i.test(normalized)) {
      return `${normalized}/chat/completions`;
    }
    return `${normalized}/v1/chat/completions`;
  };

  const buildChatCompletionsEndpoint = (value) => buildRequestEndpoint(value, 'openai');

  const sanitizeModelList = (values, maxCount = 3) => {
    const rawList = Array.isArray(values) ? values : [values];
    const out = [];
    const seen = new Set();
    for (const value of rawList) {
      const parts = String(value || '')
        .split(/[\n,]+/)
        .map((item) => normalizeText(item))
        .filter(Boolean);
      for (const name of parts) {
        const key = name.toLowerCase();
        if (!key || seen.has(key)) continue;
        seen.add(key);
        out.push(name);
        if (out.length >= Math.max(Number(maxCount) || 0, 1)) {
          return out;
        }
      }
    }
    return out;
  };

  const normalizeModelMap = (models) => {
    const source = models && typeof models === 'object' ? models : {};
    return {
      chat: sanitizeModelList(source.chat || [], 3),
      enrich: normalizeText(source.enrich || ''),
      refine: normalizeText(source.refine || ''),
      summary: normalizeText(source.summary || ''),
      rerank: normalizeText(source.rerank || ''),
    };
  };

  const isLegacySecretShape = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    return !!(
      safeSecret.summarizedLLM
      || safeSecret.chatLLMs
      || safeSecret.rerankerLLM
      || safeSecret.llmProvider
    );
  };

  const normalizeUnifiedSecret = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const llm = safeSecret.llm && typeof safeSecret.llm === 'object' ? safeSecret.llm : {};
    const requestFormat = normalizeRequestFormat(
      llm.request_format || llm.requestFormat || inferRequestFormatFromBaseUrl(llm.base_url || llm.baseUrl || ''),
    );
    const baseUrl = normalizeBaseUrlForStorage(llm.base_url || llm.baseUrl || '');
    const apiKey = normalizeText(llm.api_key || llm.apiKey || '');
    return {
      ...safeSecret,
      llm: {
        request_format: requestFormat,
        base_url: baseUrl,
        api_key: apiKey,
        models: normalizeModelMap(llm.models),
      },
    };
  };

  const migrateLegacySecret = (secret) => {
    if (!isLegacySecretShape(secret)) {
      return normalizeUnifiedSecret(secret);
    }
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const summarized = safeSecret.summarizedLLM && typeof safeSecret.summarizedLLM === 'object'
      ? safeSecret.summarizedLLM
      : {};
    const reranker = safeSecret.rerankerLLM && typeof safeSecret.rerankerLLM === 'object'
      ? safeSecret.rerankerLLM
      : {};
    const chatEntry = Array.isArray(safeSecret.chatLLMs) && safeSecret.chatLLMs.length
      ? (safeSecret.chatLLMs[0] || {})
      : {};

    const summaryBaseUrl = normalizeBaseUrlForStorage(summarized.baseUrl || '');
    const summaryApiKey = normalizeText(summarized.apiKey || '');
    const summaryModel = normalizeText(summarized.model || '');
    const chatBaseUrl = normalizeBaseUrlForStorage(chatEntry.baseUrl || '');
    const chatApiKey = normalizeText(chatEntry.apiKey || '');
    const chatModels = sanitizeModelList(chatEntry.models || [], 3);
    const rerankModel = normalizeText(reranker.model || '');

    const baseUrl = summaryBaseUrl || chatBaseUrl;
    const apiKey = summaryApiKey || chatApiKey;
    const requestFormat = normalizeRequestFormat(
      inferRequestFormatFromBaseUrl(baseUrl)
    );
    const firstChatModel = chatModels[0] || summaryModel;

    return {
      createdAt: safeSecret.createdAt || '',
      updatedAt: safeSecret.updatedAt || '',
      github: safeSecret.github && typeof safeSecret.github === 'object' ? safeSecret.github : {},
      llm: {
        request_format: requestFormat,
        base_url: baseUrl,
        api_key: apiKey,
        models: {
          chat: chatModels.length ? chatModels : sanitizeModelList([firstChatModel], 3),
          enrich: summaryModel || firstChatModel,
          refine: summaryModel || firstChatModel,
          summary: summaryModel || firstChatModel,
          rerank: rerankModel || summaryModel || firstChatModel,
        },
      },
      __legacy_migrated: true,
    };
  };

  const resolveLLMConfig = (secret) => {
    const normalized = migrateLegacySecret(secret);
    const llm = normalized.llm && typeof normalized.llm === 'object' ? normalized.llm : {};
    return {
      requestFormat: normalizeRequestFormat(llm.request_format),
      baseUrl: normalizeBaseUrlForStorage(llm.base_url || ''),
      apiKey: normalizeText(llm.api_key || ''),
      models: normalizeModelMap(llm.models),
      isLegacyMigrated: !!normalized.__legacy_migrated,
    };
  };

  const resolveChatModels = (secret) => {
    const config = resolveLLMConfig(secret);
    if (!config.baseUrl || !config.apiKey) return [];
    return config.models.chat.map((name) => ({
      name,
      apiKey: config.apiKey,
      baseUrl: config.baseUrl,
      requestFormat: config.requestFormat,
    }));
  };

  const resolveSummaryLLM = (secret) => {
    const config = resolveLLMConfig(secret);
    const model = normalizeText(config.models.summary || config.models.chat[0] || '');
    if (!config.baseUrl || !config.apiKey || !model) return null;
    return {
      requestFormat: config.requestFormat,
      baseUrl: config.baseUrl,
      apiKey: config.apiKey,
      model,
    };
  };

  const inferProviderType = (secret) => {
    return resolveLLMConfig(secret).requestFormat === 'anthropic'
      ? 'anthropic'
      : 'openai-compatible';
  };

  const getOpenAICompatiblePreset = (key) => {
    const presetKey = normalizeText(key).toLowerCase();
    const preset = OPENAI_COMPATIBLE_PRESETS[presetKey];
    if (!preset) return null;
    return {
      key: preset.key,
      label: preset.label,
      requestFormat: preset.requestFormat,
      baseUrl: preset.baseUrl,
      models: [...preset.models],
    };
  };

  const inferChatApiProfile = (baseUrl, model) => {
    const normalizedBaseUrl = normalizeBaseUrlForStorage(baseUrl || '').toLowerCase();
    const normalizedModel = normalizeText(model || '').toLowerCase();
    if (/anthropic\.com/.test(normalizedBaseUrl) || normalizedModel.startsWith('claude-')) {
      return 'anthropic';
    }
    if (
      /(^|\/\/)(api\.)?deepseek\.com(?:$|\/)/i.test(normalizedBaseUrl)
      || normalizedModel.startsWith('deepseek-')
    ) {
      return 'deepseek';
    }
    return 'generic-openai';
  };

  const shouldUseXApiKeyHeader = ({ baseUrl, model }) => {
    const normalizedBaseUrl = normalizeBaseUrlForStorage(baseUrl || '').toLowerCase();
    const normalizedModel = normalizeText(model || '').toLowerCase();
    if (
      /^minimax-/i.test(normalizedModel)
      || /(^|\/\/)api\.minimax(?:i)?\.(?:io|com)(?:$|\/)/i.test(normalizedBaseUrl)
    ) {
      return false;
    }
    return true;
  };

  const normalizeMessageContentForAnthropic = (content) => {
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) {
      return content
        .map((part) => {
          if (typeof part === 'string') return normalizeText(part);
          if (!part || typeof part !== 'object') return '';
          if (part.type === 'text') return normalizeText(part.text || '');
          return normalizeText(part.content || part.text || '');
        })
        .filter(Boolean)
        .join('\n');
    }
    if (content && typeof content === 'object') {
      return normalizeText(content.text || content.content || '');
    }
    return normalizeText(content || '');
  };

  const convertMessagesToAnthropic = (messages) => {
    const source = Array.isArray(messages) ? messages : [];
    const systemParts = [];
    const out = [];
    for (const message of source) {
      if (!message || typeof message !== 'object') continue;
      const role = normalizeText(message.role || '').toLowerCase();
      const text = normalizeMessageContentForAnthropic(message.content);
      if (!text) continue;
      if (role === 'system') {
        systemParts.push(text);
        continue;
      }
      const targetRole = role === 'assistant' ? 'assistant' : 'user';
      const last = out[out.length - 1];
      if (last && last.role === targetRole) {
        last.content += `\n\n${text}`;
      } else {
        out.push({ role: targetRole, content: text });
      }
    }
    return {
      system: systemParts.join('\n\n'),
      messages: out,
    };
  };

  const buildAnthropicSchemaHint = (responseFormat) => {
    if (!responseFormat || typeof responseFormat !== 'object') return '';
    if (responseFormat.type === 'json_schema') {
      const schemaNode = responseFormat.json_schema || {};
      const schema = schemaNode.schema || {};
      return [
        'Return only valid JSON.',
        schemaNode.name ? `Schema name: ${schemaNode.name}.` : '',
        Object.keys(schema).length ? `JSON schema: ${JSON.stringify(schema)}.` : '',
      ].filter(Boolean).join(' ');
    }
    if (responseFormat.type === 'json_object') {
      return 'Return only a valid JSON object with no markdown fences or extra text.';
    }
    return '';
  };

  const buildStreamingChatPayload = ({
    requestFormat,
    baseUrl,
    model,
    messages,
    responseFormat,
  }) => {
    const format = normalizeRequestFormat(requestFormat || inferRequestFormatFromBaseUrl(baseUrl));
    const normalizedModel = normalizeText(model);
    if (format === 'anthropic') {
      const converted = convertMessagesToAnthropic(messages);
      const schemaHint = buildAnthropicSchemaHint(responseFormat);
      const system = [converted.system, schemaHint].filter(Boolean).join('\n\n').trim();
      const payload = {
        model: normalizedModel,
        messages: converted.messages,
        stream: true,
        max_tokens: 4096,
      };
      if (system) {
        payload.system = system;
      }
      return payload;
    }

    const payload = {
      model: normalizedModel,
      messages: Array.isArray(messages) ? messages : [],
      stream: true,
    };
    const profile = inferChatApiProfile(baseUrl, model);
    if (profile === 'deepseek' && normalizedModel.toLowerCase() === 'deepseek-reasoner') {
      payload.thinking = { type: 'enabled' };
    }
    if (responseFormat != null) {
      payload.response_format = responseFormat;
    }
    return payload;
  };

  const buildConnectivityTestPayload = ({
    requestFormat,
    baseUrl,
    model,
  }) => {
    const format = normalizeRequestFormat(requestFormat || inferRequestFormatFromBaseUrl(baseUrl));
    const normalizedModel = normalizeText(model);
    if (format === 'anthropic') {
      return {
        model: normalizedModel,
        system: 'Reply with exactly: hello world',
        messages: [
          {
            role: 'user',
            content: 'hello world',
          },
        ],
        temperature: 0,
        max_tokens: 256,
      };
    }

    const normalizedBaseUrl = normalizeBaseUrlForStorage(baseUrl || '').toLowerCase();
    const wantsMaxCompletionTokens =
      /^glm-/i.test(normalizedModel)
      || /open\.bigmodel\.cn/.test(normalizedBaseUrl)
      || /thinking/i.test(normalizedModel)
      || /^kimi-/i.test(normalizedModel)
      || /^minimax-/i.test(normalizedModel)
      || normalizedModel.toLowerCase() === 'deepseek-reasoner';
    const payload = {
      model: normalizedModel,
      messages: [
        {
          role: 'system',
          content: 'Reply with exactly: hello world',
        },
        {
          role: 'user',
          content: 'hello world',
        },
      ],
      temperature: 0,
      max_tokens: 256,
    };
    if (wantsMaxCompletionTokens) {
      payload.max_completion_tokens = 256;
    }
    const profile = inferChatApiProfile(baseUrl, model);
    if (profile === 'deepseek' && normalizedModel.toLowerCase() === 'deepseek-reasoner') {
      payload.thinking = { type: 'disabled' };
    }
    return payload;
  };

  const buildChatRequest = ({
    requestFormat,
    baseUrl,
    apiKey,
    model,
    messages,
    stream,
    temperature,
    maxTokens,
    responseFormat,
  }) => {
    const format = normalizeRequestFormat(requestFormat || inferRequestFormatFromBaseUrl(baseUrl));
    const endpoint = buildRequestEndpoint(baseUrl, format);
    const normalizedApiKey = normalizeText(apiKey);
    const normalizedModel = normalizeText(model);
    const normalizedStream = !!stream;
    if (format === 'anthropic') {
      const converted = convertMessagesToAnthropic(messages);
      const schemaHint = buildAnthropicSchemaHint(responseFormat);
      const system = [converted.system, schemaHint].filter(Boolean).join('\n\n').trim();
      const body = {
        model: normalizedModel,
        messages: converted.messages,
        stream: normalizedStream,
        max_tokens: Number(maxTokens) > 0 ? Number(maxTokens) : 4096,
      };
      if (temperature != null) {
        body.temperature = Number(temperature);
      }
      if (system) {
        body.system = system;
      }
      return {
        requestFormat: format,
        endpoint,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': normalizedApiKey,
          'anthropic-version': DEFAULT_ANTHROPIC_VERSION,
          Accept: 'application/json',
        },
        body,
      };
    }

    const body = buildStreamingChatPayload({
      requestFormat: format,
      baseUrl,
      model: normalizedModel,
      messages,
      responseFormat,
    });
    body.stream = normalizedStream;
    if (temperature != null) {
      body.temperature = Number(temperature);
    }
    if (maxTokens != null) {
      body.max_tokens = Number(maxTokens);
    }
    return {
      requestFormat: format,
      endpoint,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: `Bearer ${normalizedApiKey}`,
      },
      body,
    };
  };

  const extractChatResponseText = (data, requestFormat) => {
    const format = normalizeRequestFormat(requestFormat);
    const normalizeContentPart = (part) => {
      if (typeof part === 'string') return normalizeText(part);
      if (!part || typeof part !== 'object') return '';
      return normalizeText(part.text || part.content || part.output_text || '');
    };

    if (format === 'anthropic') {
      const topContent = Array.isArray((data || {}).content) ? data.content : [];
      const topText = topContent
        .map((part) => normalizeContentPart(part))
        .filter(Boolean)
        .join('\n');
      if (topText) return topText;
      return normalizeText((data || {}).output_text || '');
    }

    const firstChoice = (((data || {}).choices || [])[0] || {});
    const message = firstChoice.message || {};
    const content = message.content;
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) {
      return content.map((part) => normalizeContentPart(part)).filter(Boolean).join('\n');
    }
    if (content && typeof content === 'object') {
      return normalizeContentPart(content);
    }

    const outputText = (data || {}).output_text;
    if (typeof outputText === 'string') return outputText;
    if (Array.isArray(outputText)) {
      return outputText.map((part) => normalizeContentPart(part)).filter(Boolean).join('\n');
    }
    return '';
  };

  return {
    DEFAULT_REQUEST_FORMAT,
    DEFAULT_ANTHROPIC_VERSION,
    OPENAI_COMPATIBLE_PRESETS,
    normalizeText,
    normalizeRequestFormat,
    inferRequestFormatFromBaseUrl,
    normalizeBaseUrlForStorage,
    buildRequestEndpoint,
    buildChatCompletionsEndpoint,
    sanitizeModelList,
    normalizeModelMap,
    isLegacySecretShape,
    normalizeUnifiedSecret,
    migrateLegacySecret,
    resolveLLMConfig,
    resolveChatModels,
    resolveSummaryLLM,
    inferProviderType,
    getOpenAICompatiblePreset,
    inferChatApiProfile,
    shouldUseXApiKeyHeader,
    convertMessagesToAnthropic,
    buildStreamingChatPayload,
    buildConnectivityTestPayload,
    buildChatRequest,
    extractChatResponseText,
  };
});
