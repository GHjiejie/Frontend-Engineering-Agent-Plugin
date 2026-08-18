# Prototype Evidence Contract

## Evidence identity

Assign one `PT-xx` to one reviewable page or visible state. Multiple crops of the same state may share a parent label but require distinct evidence rows when they prove different behavior.

Record for every item:

- Page/state name.
- Original source locator.
- Figma node/frame ID when applicable.
- Capture time and timezone.
- Stable, copyable Feishu image-block link and block ID. If Feishu cannot link the image block directly, use the uniquely paired caption block immediately adjacent to it and record that fallback explicitly.
- What is visibly confirmed.
- Behavior that remains unknown.

## Conversation images

- Use the supplied attachment or clipboard image directly when available.
- Never describe it only as “the first image” or “the screenshot above.”
- Never guess missing transitions from layout, disabled styling, or example data.
- If one image contains multiple states, split the catalog semantically even when one uploaded image is reused.

## Figma and prototype URLs

- Keep the exact node/frame URL and node ID.
- Capture only the feature scope, including meaningful alternative states when present.
- Record the capture time because the upstream design is mutable.
- A screenshot is evidence of visible UI, not proof of runtime behavior that Figma does not express.

## Storage modes

- `cloud-media`: the original uploaded evidence remains in Feishu; local Markdown keeps `PT-xx`, semantic description, and a document/block link.
- `offline-media`: additionally download media to `<output>/assets/prototype/` and reference the exported copy. The local copy remains a derivative of a specific Feishu revision.

Do not use short-lived signed URLs as durable Markdown image sources.

The recorded target must jump to the exact evidence block, not merely open the Review document. Preserve the target block during same-version updates whenever possible so downstream `PT-xx` links remain stable.
