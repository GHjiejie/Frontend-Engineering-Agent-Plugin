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
2. Insert a source index and an `原始来源附件` section before uploading evidence.
3. Insert each local or conversation-uploaded PRD/API source with the supported media-insert shortcut using file mode and a visible file card. Use selection-based placement so the card remains adjacent to its stable source heading.
4. Insert local or clipboard prototype images with image mode.
5. Save returned document, block, and file tokens in `source-manifest.md`, including stable links that open each exact source file card and image/caption block.
6. Fetch the relevant sections and resolve each stored block locator. Use the installed media preview/download workflow to verify that source attachments are retrievable and that downloaded verification bytes match the recorded SHA-256.

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
- Do not use a signed media/download URL as an ID target. Links carried by `PT-xx` must be durable document/block locators.
- For non-image sources, use the installed `docs +media-insert --type file --file-view card` workflow. Preserve the original filename and returned `file_token`; link `PRD-xx` / `API-xx` to the file-card block rather than to a temporary download URL.
- Reuse a file card when Source ID and SHA-256 are unchanged. Do not append duplicate unlabeled attachments on same-version regeneration.
