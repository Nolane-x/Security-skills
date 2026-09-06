---
name: android-webview-bridge-analysis
description: "Analyze Android WebView navigation, JavaScript bridges, origin transitions, file/content access, message channels, and native capability exposure. Use to reason about web-to-native trust boundaries with origin-aware evidence."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Android Webview Bridge Analysis

## When to use

Use when Android applications embed WebView/WebChromeClient, addJavascriptInterface, WebMessagePort/listeners, custom URL handlers, local content, or mixed remote/local navigation.

## Preconditions

1. Use a controlled app build and local test content/server.
2. Pin WebView/Chromium version and relevant settings.
3. Do not load untrusted live sites or real account content during bridge testing.

## Workflow

1. Inventory WebView settings, allowed navigation, bridge registration, message listeners, file/content access, and custom scheme handlers.
2. Map each native-exposed method/capability to the document origins that can reach it over time, including redirects and subframes.
3. Check whether origin verification occurs at message receipt and after navigation, not only at initial load.
4. Trace bridge parameters into file, intent, token, IPC, or privileged app operations.
5. Review local-file/content URI interactions and mixed-content or universal-access settings as separate trust transitions.
6. Use a local benign page to prove reachability and negative controls for disallowed origins.
7. Treat JavaScript execution and native capability reachability as separate evidence stages.

## Evidence contract

Record WebView version/settings, bridge/message API, origin/frame, navigation path, native capability, and allowed/denied control outcomes. Do not equate arbitrary page content with native code execution.

## Stop conditions

Stop if origin control cannot be isolated locally, testing would expose real credentials/cookies, or required navigation leaves the authorized environment.

## Output

```text
WebView/version:
bridge or message surface:
origin/frame model:
navigation transitions:
native capability:
control outcomes:
evidence status:
```
