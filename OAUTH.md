# OAuth Architecture

## Core Abstraction (`packages/ai/src/utils/oauth/`)

**`OAuthProviderInterface`** (types.ts) defines the contract every provider implements:
- `login(callbacks)` — runs the auth flow, returns `OAuthCredentials`
- `refreshToken(credentials)` — refreshes expired tokens
- `getApiKey(credentials)` — converts credentials to an API key string for use in requests
- `modifyModels?()` — optional hook to update model metadata (e.g. base URLs)

**`OAuthCredentials`** stores: `{ access, refresh, expires, ...extras }`.

---

## Registered Providers (`index.ts`)

Five built-in providers, each in its own file:

| Provider | File | Auth Flow |
|---|---|---|
| Anthropic (Claude Pro/Max) | `anthropic.ts` | PKCE + local callback server on port 53692 |
| GitHub Copilot | `github-copilot.ts` | Device code flow (no redirect server) |
| Google Gemini CLI | `google-gemini-cli.ts` | PKCE + local callback server on port 8085 |
| Google Antigravity | `google-antigravity.ts` | PKCE + local callback server on port 51121 |
| OpenAI Codex (ChatGPT) | `openai-codex.ts` | PKCE + local callback server on port 1455 |

A `Map`-based registry allows custom providers via `registerOAuthProvider()`.

---

## Auth Flows

### PKCE flow (Anthropic, Google, OpenAI Codex)

1. Generate a PKCE verifier/challenge via Web Crypto API (`pkce.ts`)
2. Open authorization URL in browser
3. Spin up a local `http.createServer` to catch the redirect callback with the `code`
4. Exchange `code + verifier` for access/refresh tokens at the provider's token endpoint
5. Store credentials; serve success/error HTML pages (`oauth-page.ts`)
6. If a local server can't start, fall back to manual code input via `onManualCodeInput` callback

### Device code flow (GitHub Copilot)

1. Request a device code from GitHub
2. Show `user_code` + verification URL to the user
3. Poll GitHub's token endpoint until the user completes authorization or it times out
4. Exchange for a short-lived Copilot token by calling the Copilot internal token API
5. Extract the API base URL from the token's `proxy-ep` field

---

## Token Lifecycle (`getOAuthApiKey`)

```
credentials in storage → check expiry → auto-refresh if expired → call provider.getApiKey() → return string
```

This is used at call time so callers always get a valid token without managing refresh themselves.

---

## Credential Storage

Credentials are persisted to `~/.pi/agent/auth.json` (permissions: `0600`), keyed by provider ID. Each entry has `type: "oauth"` plus the `OAuthCredentials` fields. The CLI (`src/cli.ts`) handles the interactive login flow and writes to this file.
