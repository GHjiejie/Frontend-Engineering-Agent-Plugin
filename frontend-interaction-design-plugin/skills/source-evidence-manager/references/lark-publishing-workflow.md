# lark-cli Evidence Workflow

Use the installed `lark-cli` as the first choice for Feishu operations.

## Mandatory preparation

Before running document commands:

1. Run `lark-cli skills read lark-doc`.
2. Read `lark-shared` and every operation-specific reference required by that installed skill.
3. Confirm authentication and the existing document permissions.
4. Use explicit `--api-version v2` for document create, fetch, and update commands when required by the installed skill.

The installed CLI guidance is authoritative when command flags differ from examples below.

## Document lifecycle

1. Create one document after Gate #2, titled `[Frontend Design] <Feature> / <Version>`, or reuse the current version's documented token.
2. Insert a source index before uploading evidence.
3. Insert local or clipboard images with the supported media-insert shortcut.
4. Save returned document, block, and file tokens in `source-manifest.md`.
5. Fetch the relevant section to verify every uploaded image and caption.

## Safety

- Treat document creation, updates, and media insertion as writes authorized only inside the confirmed feature/version workflow.
- Do not create a replacement document merely because an update fails.
- Stop on permission, authentication, missing-scope, or not-found errors; follow CLI hints instead of switching identities repeatedly.
- Never broaden document sharing automatically.
- Do not expose tokens that grant access beyond ordinary document locators.

## Media

- Prefer clipboard insertion only when the user supplied an image through the clipboard; otherwise use the real local file.
- A URL image may be inserted through supported document update syntax or downloaded first according to the installed guidance.
- Download media only for explicit offline export or verification; Feishu remains the default image store.
