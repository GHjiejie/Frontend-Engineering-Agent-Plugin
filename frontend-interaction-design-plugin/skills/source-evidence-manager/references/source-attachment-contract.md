# Source Attachment Contract

Use this contract when a PRD, API contract, permission matrix, data dictionary, or other review source is supplied as a local or conversation-uploaded file.

## Choose the durable source form

- A user-uploaded or local file must be inserted into the confirmed Feishu Review document as a file card. Preserve the original bytes and filename.
- An already-accessible canonical cloud document may remain a stable source link. Add a file snapshot when the source is mutable, reviewer access is uncertain, or the supplied file is the version actually reviewed.
- For a repository source, attach only the exact in-scope contract file. Do not archive or upload a directory, repository, build output, credential file, or unrelated source tree unless the developer explicitly requests that scope.
- Keep a concise source summary in the Review document. An attachment does not replace the context reviewers need before opening it.

## Inspect before upload

Use the exact supplied attachment or confirmed local path; never guess a path for an unavailable conversation file. Record the source ID, original filename, media type, byte size, SHA-256 digest, version or revision, and capture time. Do not upload secrets, credentials, private keys, session material, production configuration, or fields outside the confirmed review scope. If the file is unavailable or safe inclusion cannot be determined, block Source Gate and ask for the file to be reattached or sanitized.

## Publish the attachment

1. Maintain an `原始来源附件` section in the current feature/version Review document.
2. Give each attachment a canonical heading such as `PRD-01 系统配置需求` or `API-01 Console OpenAPI`, followed by a short scope summary.
3. Insert the original file with the installed `lark-cli docs +media-insert` file mode and a visible file card. Place it adjacent to its canonical heading rather than appending an unlabeled file at the document end.
4. Record the returned `file_token`, `block_id`, original filename, and the stable `<review-document-url>#<block_id>` locator. Never use a signed download URL as the canonical link.
5. Link the Source ID, source title, and explicit `查看/下载原文件` action in source tables to the exact file-card block. Link IDs individually when several sources appear together.
6. Reuse an existing attachment when the source ID and SHA-256 match. When content changes, record the new digest/version, replace the canonical attachment target, and avoid leaving two unlabeled active cards for the same ID.

The file card is the download surface. The Source ID link navigates to that card; it is not itself an expiring direct-download URL.

## Verify reviewer access

- Fetch the final document with block IDs and confirm the stored block belongs to the expected document and source ID.
- Use the installed media preview/download workflow to verify that the file token is readable. For a downloaded verification copy, compare its SHA-256 with the recorded source digest and remove only that known temporary copy afterward.
- Preserve the document's existing permissions. Do not broaden sharing automatically.
- Record `Verified` only after the file card resolves and the uploaded bytes can be retrieved. Otherwise mark the source inaccessible and block Source Gate.

## Gate rule

A local or conversation-uploaded source represented only by a filename, repository path, static table cell, or prose summary is not durable evidence. Source Gate cannot pass until the exact file is available as a verified Feishu attachment or the developer explicitly replaces it with another durable canonical source.
