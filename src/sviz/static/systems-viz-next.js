const NEXT_STYLES = String.raw`
  :host {
    --sv-bg: #fbfbfc;
    --sv-panel: #ffffff;
    --sv-panel-soft: #f5f6f8;
    --sv-text: #1b1d21;
    --sv-muted: #6d7480;
    --sv-border: #dfe2e7;
    --sv-primary: #5069e8;
    --sv-transfer: #d98624;
    --sv-compute: #249873;
    --sv-state: #b34f78;
    --sv-selection: #7a55c5;
    --sv-danger: #c43f4d;
    display: block;
    width: 100%;
    height: 100%;
    min-height: 520px;
    color: var(--sv-text);
    font: 13px/1.45 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  :host([theme="dark"]) {
    --sv-bg: #111318;
    --sv-panel: #171a20;
    --sv-panel-soft: #20242b;
    --sv-text: #f4f5f7;
    --sv-muted: #a3a9b4;
    --sv-border: #303641;
    --sv-primary: #8797ff;
    --sv-transfer: #f0a54b;
    --sv-compute: #49c99d;
    --sv-state: #e477a2;
    --sv-selection: #ad91ec;
    --sv-danger: #ff7d89;
  }
  @media (prefers-color-scheme: dark) {
    :host([theme="auto"]) {
      --sv-bg: #111318;
      --sv-panel: #171a20;
      --sv-panel-soft: #20242b;
      --sv-text: #f4f5f7;
      --sv-muted: #a3a9b4;
      --sv-border: #303641;
      --sv-primary: #8797ff;
      --sv-transfer: #f0a54b;
      --sv-compute: #49c99d;
      --sv-state: #e477a2;
      --sv-selection: #ad91ec;
      --sv-danger: #ff7d89;
    }
  }
  * { box-sizing: border-box; }
  button, input, textarea { font: inherit; color: inherit; }
  .root {
    height: 100%;
    min-height: 520px;
    display: grid;
    grid-template-rows: auto minmax(0, 1fr) auto;
    overflow: hidden;
    border: 1px solid var(--sv-border);
    border-radius: 11px;
    background: var(--sv-bg);
  }
  .head {
    width: 100%;
    min-width: 0;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    padding: 13px 14px 11px;
    border-bottom: 1px solid var(--sv-border);
    overflow: hidden;
  }
  .heading { min-width: 0; flex: 1 1 0; }
  .title { margin: 0 0 2px; font-size: 16px; line-height: 1.25; font-weight: 650; letter-spacing: -.01em; }
  .subtitle { color: var(--sv-muted); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .head-actions { display: flex; align-items: center; gap: 9px; flex: 0 0 auto; }
  .layout-check-controls { display: flex; align-items: center; gap: 6px; }
  .layout-check-status { max-width: 112px; overflow: hidden; color: var(--sv-muted); font-size: 10px; text-overflow: ellipsis; white-space: nowrap; }
  .layout-check-status[data-state="fail"] { color: var(--sv-danger); }
  .layout-check-status[data-state="pass"] { color: var(--sv-compute); }
  .persistence-controls { display: flex; align-items: center; gap: 6px; }
  .persistence-status { max-width: 104px; overflow: hidden; color: var(--sv-muted); font-size: 10px; text-overflow: ellipsis; white-space: nowrap; }
  .persistence-status[data-state="conflict"], .persistence-status[data-state="error"] { color: var(--sv-danger); }
  .tabs { display: flex; align-items: center; gap: 2px; flex: 0 0 auto; }
  .tab, .step-button {
    appearance: none;
    border: 1px solid transparent;
    border-radius: 7px;
    background: transparent;
    cursor: pointer;
  }
  .tab { min-height: 32px; padding: 5px 9px; color: var(--sv-muted); }
  .tab:hover, .step-button:hover { background: color-mix(in srgb, var(--sv-text) 6%, transparent); }
  .tab:focus-visible, .step-button:focus-visible { outline: 2px solid var(--sv-primary); outline-offset: 2px; }
  .tab[aria-selected="true"] { border-color: var(--sv-border); background: var(--sv-panel); color: var(--sv-text); }
  .workspace { min-width: 0; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(270px, 320px); }
  .stage { width: 100%; min-width: 0; min-height: 0; overflow: auto; background: var(--sv-panel); }
  .panel[hidden] { display: none; }
  .canvas { width: 100%; height: 100%; min-height: 430px; }
  .system-panel { width: 100%; height: 100%; min-height: 430px; display: grid; grid-template-rows: auto minmax(0, 1fr); }
  .system-toolbar {
    min-width: 0;
    min-height: 42px;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 5px 9px;
    border-bottom: 1px solid var(--sv-border);
    background: var(--sv-bg);
  }
  .tool-label { margin-right: 2px; color: var(--sv-muted); font-size: 11px; }
  .tool-button {
    min-width: 30px;
    height: 30px;
    padding: 0 8px;
    border: 1px solid var(--sv-border);
    border-radius: 6px;
    background: var(--sv-panel);
    cursor: pointer;
  }
  .tool-button:hover { background: var(--sv-panel-soft); }
  .tool-button:focus-visible { outline: 2px solid var(--sv-primary); outline-offset: 1px; }
  .tool-button:disabled { opacity: .4; cursor: default; }
  .tool-button[aria-pressed="true"] { border-color: var(--sv-primary); background: color-mix(in srgb, var(--sv-primary) 10%, var(--sv-panel)); }
  .tool-value { min-width: 42px; text-align: center; color: var(--sv-muted); font-size: 11px; font-variant-numeric: tabular-nums; }
  .tool-help { min-width: 0; margin-left: 6px; overflow: hidden; color: var(--sv-muted); font-size: 11px; text-overflow: ellipsis; white-space: nowrap; }
  .tool-reset { margin-left: auto; }
  .system-surface, .timeline-surface { position: relative; min-width: 0; min-height: 0; }
  .system-surface { height: 100%; }
  .timeline-surface { width: 100%; height: 100%; }
  .pin-layer { position: absolute; inset: 0; z-index: 4; pointer-events: none; overflow: hidden; }
  .annotation-pin {
    position: absolute;
    width: 23px;
    height: 23px;
    display: grid;
    place-items: center;
    padding: 0;
    border: 2px solid var(--sv-panel);
    border-radius: 50%;
    background: var(--sv-state);
    color: #fff;
    box-shadow: 0 1px 5px color-mix(in srgb, var(--sv-text) 24%, transparent);
    font-size: 10px;
    font-weight: 750;
    line-height: 1;
    pointer-events: auto;
    cursor: pointer;
  }
  .annotation-pin[data-status="resolved"] { background: var(--sv-compute); opacity: .8; }
  .annotation-pin[aria-current="true"] { outline: 2px solid var(--sv-selection); outline-offset: 2px; }
  .annotation-pin:focus-visible { outline: 2px solid var(--sv-primary); outline-offset: 2px; }
  svg { width: 100%; height: 100%; min-height: 0; display: block; }
  svg text { fill: var(--sv-text); font-family: ui-sans-serif, system-ui, sans-serif; }
  .timeline-label { pointer-events: none; }
  .edge-layer, .moving-layer { pointer-events: none; }
  .edge-layer [data-select] { pointer-events: auto; }
  .edge-layer [data-edge-hit] { pointer-events: stroke; }
  .moving-layer [data-select] { pointer-events: auto; }
  .edge-adjust-layer [data-drag-edge] { cursor: move; touch-action: none; }
  .edge-label { paint-order: stroke; stroke: var(--sv-panel); stroke-width: 5px; stroke-linejoin: round; }
  [data-drag-place] { cursor: grab; touch-action: none; }
  [data-drag-place][data-dragging="true"] { cursor: grabbing; }
  [data-resize-place] { cursor: nwse-resize; touch-action: none; }
  [data-select] { cursor: pointer; }
  [data-select]:focus-visible { outline: none; }
  [data-select]:focus-visible rect, [data-drag-place]:focus-visible rect, [data-resize-place]:focus-visible rect, [data-drag-edge]:focus-visible circle { stroke: var(--sv-selection); stroke-width: 3; }
  .code {
    margin: 0;
    min-height: 430px;
    padding: 16px 18px;
    overflow: auto;
    color: var(--sv-text);
    background: var(--sv-panel-soft);
    font: 11px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    white-space: pre;
    tab-size: 2;
  }
  .narrative-panel {
    min-width: 0;
    min-height: 0;
    overflow: auto;
    padding: 14px;
    border-left: 1px solid var(--sv-border);
    background: var(--sv-bg);
  }
  .content-heading, .annotation-heading { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .content-heading h3, .annotation-heading h4 { margin: 0; font-size: 13px; line-height: 1.3; }
  .content-action {
    min-height: 28px;
    padding: 3px 8px;
    border: 1px solid var(--sv-border);
    border-radius: 6px;
    background: var(--sv-panel);
    cursor: pointer;
    font-size: 11px;
  }
  .content-action:hover { background: var(--sv-panel-soft); }
  .content-action:focus-visible, .narrative-input:focus-visible, .annotation-input:focus-visible { outline: 2px solid var(--sv-primary); outline-offset: 1px; }
  .content-action:disabled { opacity: .45; cursor: default; }
  .narrative-preview { min-height: 92px; margin-top: 10px; color: var(--sv-text); overflow-wrap: anywhere; }
  .narrative-preview > :first-child { margin-top: 0; }
  .narrative-preview > :last-child { margin-bottom: 0; }
  .narrative-preview h1, .narrative-preview h2, .narrative-preview h3 { margin: .8em 0 .35em; line-height: 1.3; }
  .narrative-preview h1 { font-size: 16px; }
  .narrative-preview h2 { font-size: 15px; }
  .narrative-preview h3 { font-size: 14px; }
  .narrative-preview p, .narrative-preview ul, .narrative-preview ol, .narrative-preview blockquote, .narrative-preview pre { margin: .6em 0; }
  .narrative-preview ul, .narrative-preview ol { padding-left: 20px; }
  .narrative-preview blockquote { padding-left: 9px; border-left: 3px solid var(--sv-border); color: var(--sv-muted); }
  .narrative-preview code { padding: 1px 3px; border-radius: 3px; background: var(--sv-panel-soft); font: 11px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace; }
  .narrative-preview pre { padding: 8px; overflow: auto; border: 1px solid var(--sv-border); border-radius: 6px; background: var(--sv-panel-soft); }
  .narrative-preview pre code { padding: 0; background: transparent; }
  .narrative-preview a { color: var(--sv-primary); }
  .narrative-input, .annotation-input {
    width: 100%;
    border: 1px solid var(--sv-border);
    border-radius: 6px;
    background: var(--sv-panel);
  }
  .narrative-input { min-height: 130px; margin-top: 10px; padding: 9px; resize: vertical; font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; }
  .markdown-hint { margin-top: 5px; color: var(--sv-muted); font-size: 10px; }
  .annotation-section { margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--sv-border); }
  .annotation-help, .annotation-empty { margin: 7px 0 0; color: var(--sv-muted); font-size: 10px; }
  .annotation-list { display: grid; gap: 7px; margin-top: 9px; }
  .annotation-card { border: 1px solid var(--sv-border); border-radius: 7px; background: var(--sv-panel); overflow: hidden; }
  .annotation-card[data-active="true"] { border-color: var(--sv-selection); }
  .annotation-summary { display: grid; grid-template-columns: 24px minmax(0, 1fr) auto; align-items: center; gap: 7px; padding: 7px; }
  .annotation-open { display: contents; cursor: pointer; }
  .annotation-number { width: 21px; height: 21px; display: grid; place-items: center; border-radius: 50%; background: var(--sv-state); color: #fff; font-size: 10px; font-weight: 750; }
  .annotation-card[data-status="resolved"] .annotation-number { background: var(--sv-compute); }
  .annotation-copy { min-width: 0; }
  .annotation-title { overflow: hidden; font-size: 11px; font-weight: 650; text-overflow: ellipsis; white-space: nowrap; }
  .annotation-anchor { overflow: hidden; color: var(--sv-muted); font-size: 10px; text-overflow: ellipsis; white-space: nowrap; }
  .status-switch { min-width: 69px; min-height: 26px; padding: 2px 6px; border: 1px solid var(--sv-border); border-radius: 999px; background: var(--sv-panel-soft); cursor: pointer; font-size: 10px; }
  .status-switch[aria-checked="true"] { border-color: var(--sv-compute); color: var(--sv-compute); }
  .annotation-editor { display: grid; gap: 6px; padding: 0 7px 8px 38px; }
  .annotation-editor-actions { display: flex; justify-content: flex-end; }
  .annotation-delete { color: var(--sv-danger); }
  .annotation-delete:hover { border-color: color-mix(in srgb, var(--sv-danger) 55%, var(--sv-border)); }
  .annotation-input { padding: 6px 7px; font-size: 11px; }
  textarea.annotation-input { min-height: 64px; resize: vertical; }
  .foot {
    min-height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 7px 9px 7px 14px;
    border-top: 1px solid var(--sv-border);
    background: var(--sv-bg);
  }
  .checkpoint { min-width: 0; }
  .checkpoint-title { font-weight: 650; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .checkpoint-detail { color: var(--sv-muted); font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .step-controls { display: flex; align-items: center; gap: 2px; flex: 0 0 auto; }
  .step-index { min-width: 48px; text-align: right; color: var(--sv-muted); font-variant-numeric: tabular-nums; }
  .step-button { width: 36px; height: 36px; font-size: 17px; }
  .step-button:disabled { opacity: .35; cursor: default; }
  .error { min-height: 360px; display: grid; place-items: center; padding: 24px; color: #c43f4d; }
  @media (max-width: 620px) {
    :host { min-height: 660px; }
    .root { min-height: 660px; }
    .head { display: block; }
    .subtitle { white-space: normal; }
    .head-actions { margin-top: 10px; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; }
    .tabs { overflow-x: auto; }
    .workspace { display: block; overflow: auto; }
    .stage { min-height: 560px; overflow: visible; }
    .canvas, .code { min-height: 560px; }
    .system-panel { min-height: 560px; }
    .system-toolbar { flex-wrap: wrap; }
    .tool-help { order: 3; width: 100%; margin: 0 2px; }
    .foot { align-items: flex-start; }
    .checkpoint-title, .checkpoint-detail { white-space: normal; }
    .narrative-panel { min-height: 260px; overflow: visible; border-top: 1px solid var(--sv-border); border-left: 0; }
  }
`;

const escapeText = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

function safeMarkdownHref(value) {
  const href = String(value || "").replaceAll("&amp;", "&").trim();
  return /^(https?:|mailto:|#|\/|\.\.?\/)/i.test(href) ? escapeText(href) : "#";
}

function renderInlineMarkdown(value) {
  const code = [];
  let rendered = escapeText(value).replace(/`([^`\n]+)`/g, (_, content) => {
    const token = `@@SVIZ-CODE-${code.length}@@`;
    code.push(`<code>${content}</code>`);
    return token;
  });
  rendered = rendered
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label, href) => `<a href="${safeMarkdownHref(href)}" target="_blank" rel="noreferrer">${label}</a>`)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/__([^_]+)__/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/_([^_]+)_/g, "<em>$1</em>");
  code.forEach((content, index) => { rendered = rendered.replace(`@@SVIZ-CODE-${index}@@`, content); });
  return rendered;
}

function renderMarkdown(value) {
  const lines = String(value || "").replaceAll("\r\n", "\n").split("\n");
  const output = [];
  let paragraph = [];
  let list = null;
  let code = null;

  const flushParagraph = () => {
    if (!paragraph.length) return;
    output.push(`<p>${paragraph.map(renderInlineMarkdown).join("<br>")}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (!list) return;
    output.push(`<${list.type}>${list.items.map(item => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</${list.type}>`);
    list = null;
  };
  const flushCode = () => {
    if (code === null) return;
    output.push(`<pre><code>${escapeText(code.join("\n"))}</code></pre>`);
    code = null;
  };

  for (const line of lines) {
    if (/^```/.test(line)) {
      flushParagraph();
      flushList();
      if (code === null) code = [];
      else flushCode();
      continue;
    }
    if (code !== null) {
      code.push(line);
      continue;
    }
    if (!line.trim()) {
      flushParagraph();
      flushList();
      continue;
    }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      flushList();
      const level = heading[1].length;
      output.push(`<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }
    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flushParagraph();
      flushList();
      output.push(`<blockquote>${renderInlineMarkdown(quote[1])}</blockquote>`);
      continue;
    }
    const unordered = line.match(/^\s*[-*+]\s+(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (unordered || ordered) {
      flushParagraph();
      const type = unordered ? "ul" : "ol";
      if (list && list.type !== type) flushList();
      if (!list) list = { type, items: [] };
      list.items.push((unordered || ordered)[1]);
      continue;
    }
    flushList();
    paragraph.push(line);
  }
  flushParagraph();
  flushList();
  flushCode();
  return output.join("") || '<p class="annotation-empty">No narrative has been written for this checkpoint.</p>';
}

const clampValue = (value, minimum, maximum) => Math.min(maximum, Math.max(minimum, value));

function compactNumber(value) {
  const number = Number(value || 0);
  if (Math.abs(number) >= 1024 * 1024) return `${(number / (1024 * 1024)).toFixed(number % (1024 * 1024) ? 1 : 0)} Mi`;
  if (Math.abs(number) >= 1024) return `${(number / 1024).toFixed(number % 1024 ? 1 : 0)} Ki`;
  return Number.isInteger(number) ? String(number) : number.toFixed(2).replace(/0+$/, "").replace(/\.$/, "");
}

function compactBytes(value) {
  const number = Number(value || 0);
  if (Math.abs(number) >= 1024 * 1024) return `${(number / (1024 * 1024)).toFixed(number % (1024 * 1024) ? 1 : 0)} MiB`;
  if (Math.abs(number) >= 1024) return `${(number / 1024).toFixed(number % 1024 ? 1 : 0)} KiB`;
  return `${Number.isInteger(number) ? number : number.toFixed(2)} B`;
}

function fitTimelineLabel(value, availableWidth, fontSize) {
  const characters = Array.from(String(value || ""));
  const maxCharacters = Math.floor(Math.max(0, availableWidth) / Math.max(1, fontSize * .58));
  if (maxCharacters < 4) return { text: "", fit: "hidden" };
  if (characters.length <= maxCharacters) return { text: characters.join(""), fit: "full" };
  return { text: `${characters.slice(0, Math.max(3, maxCharacters - 1)).join("")}…`, fit: "truncated" };
}

function visibleRectangle(element) {
  if (!element || element.getClientRects().length === 0) return null;
  const rect = element.getBoundingClientRect();
  if (rect.width <= .5 || rect.height <= .5) return null;
  return {
    left: rect.left,
    top: rect.top,
    right: rect.right,
    bottom: rect.bottom,
    width: rect.width,
    height: rect.height,
  };
}

function rectangleIntersection(first, second, tolerance = 1) {
  const width = Math.min(first.right, second.right) - Math.max(first.left, second.left);
  const height = Math.min(first.bottom, second.bottom) - Math.max(first.top, second.top);
  if (width <= tolerance || height <= tolerance) return null;
  return { width, height, area: width * height };
}

function rectangleContains(container, content, tolerance = 1) {
  return content.left >= container.left - tolerance
    && content.top >= container.top - tolerance
    && content.right <= container.right + tolerance
    && content.bottom <= container.bottom + tolerance;
}

function routeConnection(fromBox, toBox, obstacles, canvas, routeIndex, profileName, label, adjustment = { x: 0, y: 0 }) {
  const gap = 7;
  const offsetX = Number(adjustment.x || 0) * canvas.width;
  const offsetY = Number(adjustment.y || 0) * canvas.height;
  const manuallyAdjusted = Math.abs(offsetX) > .01 || Math.abs(offsetY) > .01;
  const from = { x: fromBox.x + fromBox.w / 2, y: fromBox.y + fromBox.h / 2 };
  const to = { x: toBox.x + toBox.w / 2, y: toBox.y + toBox.h / 2 };
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const horizontal = Math.abs(dx) >= Math.abs(dy);
  let start;
  let end;
  let blocked;

  if (horizontal) {
    const direction = dx >= 0 ? 1 : -1;
    start = { x: from.x + direction * (fromBox.w / 2 + gap), y: from.y };
    end = { x: to.x - direction * (toBox.w / 2 + gap), y: to.y };
    const corridor = {
      x: Math.min(start.x, end.x),
      y: Math.min(start.y, end.y) - 8,
      w: Math.abs(end.x - start.x),
      h: Math.abs(end.y - start.y) + 16,
    };
    blocked = obstacles.some(box => corridor.x < box.x + box.w && corridor.x + corridor.w > box.x && corridor.y < box.y + box.h && corridor.y + corridor.h > box.y);
  } else {
    const direction = dy >= 0 ? 1 : -1;
    start = { x: from.x, y: from.y + direction * (fromBox.h / 2 + gap) };
    end = { x: to.x, y: to.y - direction * (toBox.h / 2 + gap) };
    const corridor = {
      x: Math.min(start.x, end.x) - 8,
      y: Math.min(start.y, end.y),
      w: Math.abs(end.x - start.x) + 16,
      h: Math.abs(end.y - start.y),
    };
    blocked = obstacles.some(box => corridor.x < box.x + box.w && corridor.x + corridor.w > box.x && corridor.y < box.y + box.h && corridor.y + corridor.h > box.y);
  }

  const exposedLength = horizontal ? Math.abs(end.x - start.x) : Math.abs(end.y - start.y);
  const labelLength = Math.min(160, Math.max(54, String(label || "").length * 6 + 16));
  if (!blocked && exposedLength >= labelLength) {
    if (horizontal) {
      const middle = (start.x + end.x) / 2;
      const handle = {
        x: clampValue(middle + offsetX, 18, canvas.width - 18),
        y: clampValue((start.y + end.y) / 2 + offsetY, 18, canvas.height - 18),
      };
      return {
        path: manuallyAdjusted
          ? `M ${start.x} ${start.y} L ${handle.x} ${handle.y} L ${end.x} ${end.y}`
          : `M ${start.x} ${start.y} C ${middle} ${start.y} ${middle} ${end.y} ${end.x} ${end.y}`,
        label: { x: handle.x, y: handle.y - 10 },
        handle,
        external: false,
      };
    }
    const middle = (start.y + end.y) / 2;
    const handle = {
      x: clampValue((start.x + end.x) / 2 + offsetX, 18, canvas.width - 18),
      y: clampValue(middle + offsetY, 18, canvas.height - 18),
    };
    return {
      path: manuallyAdjusted
        ? `M ${start.x} ${start.y} L ${handle.x} ${handle.y} L ${end.x} ${end.y}`
        : `M ${start.x} ${start.y} C ${start.x} ${middle} ${end.x} ${middle} ${end.x} ${end.y}`,
      label: { x: handle.x, y: handle.y - 10 },
      handle,
      external: false,
    };
  }

  const lane = Math.floor(routeIndex / 2);
  if (profileName === "wide") {
    const above = routeIndex % 2 === 0;
    const automaticY = above
      ? Math.min(fromBox.y, toBox.y, ...obstacles.map(box => box.y)) - 22 - lane * 32
      : Math.max(fromBox.y + fromBox.h, toBox.y + toBox.h, ...obstacles.map(box => box.y + box.h)) + 22 + lane * 32;
    const edgeY = clampValue(automaticY + offsetY, 18, canvas.height - 18);
    start = { x: from.x, y: above ? fromBox.y - gap : fromBox.y + fromBox.h + gap };
    end = { x: to.x, y: above ? toBox.y - gap : toBox.y + toBox.h + gap };
    const labelX = clampValue((start.x + end.x) / 2 + offsetX, 18, canvas.width - 18);
    return {
      path: `M ${start.x} ${start.y} L ${start.x} ${edgeY} L ${end.x} ${edgeY} L ${end.x} ${end.y}`,
      label: { x: labelX, y: edgeY + (above ? -10 : 18) },
      handle: { x: labelX, y: edgeY },
      external: true,
    };
  }

  const right = routeIndex % 2 === 0;
  const automaticX = right
    ? Math.max(fromBox.x + fromBox.w, toBox.x + toBox.w, ...obstacles.map(box => box.x + box.w)) + 14 + lane * 18
    : Math.min(fromBox.x, toBox.x, ...obstacles.map(box => box.x)) - 14 - lane * 18;
  const edgeX = clampValue(automaticX + offsetX, 24, canvas.width - 24);
  start = { x: right ? fromBox.x + fromBox.w + gap : fromBox.x - gap, y: from.y };
  end = { x: right ? toBox.x + toBox.w + gap : toBox.x - gap, y: to.y };
  const labelY = clampValue((start.y + end.y) / 2 + offsetY, 18, canvas.height - 18);
  return {
    path: `M ${start.x} ${start.y} L ${edgeX} ${start.y} L ${edgeX} ${end.y} L ${end.x} ${end.y}`,
    label: { x: edgeX + (right ? 10 : -10), y: labelY },
    handle: { x: edgeX, y: labelY },
    external: true,
    verticalLabel: true,
  };
}

class SystemsVizNext extends HTMLElement {
  static get observedAttributes() { return ["src", "initial-view", "initial-cursor", "theme", "shape-scale", "state-src", "visualization-id"]; }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.data = null;
    this.view = this.getAttribute("initial-view") || "system";
    this.cursorIndex = 0;
    this.selection = null;
    this.placeOffsets = {};
    this.placeScales = {};
    this.edgeOffsets = {};
    this.shapeScale = 1;
    this.edgeEditMode = false;
    this.dragState = null;
    this.resizeState = null;
    this.edgeDragState = null;
    this.narrativeDrafts = {};
    this.baseNarratives = {};
    this.narrativeEditing = false;
    this.annotations = [];
    this.baseAnnotations = [];
    this.deletedAnnotationIds = new Set();
    this.activeAnnotation = null;
    this.localAnnotationCounter = 0;
    this.stateRevision = 0;
    this.stateDirty = false;
    this.stateStatus = "unconfigured";
    this.stateBaseMismatch = false;
    this.layoutCheckState = "idle";
    this.layoutCheckReport = null;
    this.layoutCheckPromise = null;
    this.pinFrame = null;
    this.resizeObserver = new ResizeObserver(() => {
      this.renderActivePanel();
      const width = Math.round(this.getBoundingClientRect().width);
      if (this.layoutCheckReport && this.layoutCheckReport.width !== width) {
        this.layoutCheckState = "idle";
        this.layoutCheckReport = null;
        this.updateLayoutCheckControls();
      }
    });
  }

  connectedCallback() {
    this.load();
  }

  disconnectedCallback() {
    this.resizeObserver.disconnect();
    if (this.pinFrame !== null) cancelAnimationFrame(this.pinFrame);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (!this.isConnected || oldValue === newValue) return;
    if (name === "src") this.load();
    if (name === "initial-view" && newValue) {
      this.view = newValue;
      this.render();
    }
    if (name === "shape-scale" && newValue) this.setShapeScale(Number(newValue), false);
    if (name === "state-src" && this.data) this.loadViewerState();
    if (name === "visualization-id" && this.data && newValue && newValue !== this.data.visualization_id) {
      this.stateStatus = "error";
      this.updatePersistenceControls("Visualization ID mismatch");
    }
  }

  async load() {
    try {
      const source = this.getAttribute("src");
      if (source) {
        const response = await fetch(source);
        if (!response.ok) throw new Error(`Unable to load compiled visualization (${response.status})`);
        this.data = await response.json();
      } else {
        const inline = this.querySelector('script[type="application/vnd.sviz+json"]');
        if (!inline) throw new Error("Provide src or inline compiled JSON");
        this.data = JSON.parse(inline.textContent || "{}");
      }
      if (this.data.format !== "sviz-display" || this.data.format_version !== "0.2-draft") {
        throw new Error("This component requires sviz-display 0.2-draft");
      }
      const requestedId = this.getAttribute("visualization-id");
      if (requestedId && requestedId !== this.data.visualization_id) {
        throw new Error(`visualization-id ${requestedId} does not match compiled ID ${this.data.visualization_id}`);
      }
      const requested = Number(this.getAttribute("initial-cursor") || 0);
      this.cursorIndex = clampValue(Number.isFinite(requested) ? requested : 0, 0, this.checkpoints.length - 1);
      const requestedScale = Number(this.getAttribute("shape-scale") || 1);
      this.shapeScale = clampValue(Number.isFinite(requestedScale) ? requestedScale : 1, .7, 1.4);
      this.baseNarratives = Object.fromEntries(this.checkpoints.map(checkpoint => [
        checkpoint.id,
        checkpoint.narrative ?? checkpoint.detail ?? "",
      ]));
      this.narrativeDrafts = structuredClone(this.baseNarratives);
      this.baseAnnotations = structuredClone(this.data.content?.annotations || []).map(annotation => ({ ...annotation, origin: annotation.origin || "authored" }));
      this.annotations = structuredClone(this.baseAnnotations);
      this.deletedAnnotationIds = new Set();
      this.activeAnnotation = null;
      this.localAnnotationCounter = 0;
      this.stateRevision = 0;
      this.stateDirty = false;
      this.stateStatus = this.getAttribute("state-src") ? "loading" : "unconfigured";
      this.stateBaseMismatch = false;
      this.layoutCheckState = "idle";
      this.layoutCheckReport = null;
      this.layoutCheckPromise = null;
      for (const id of this.data.display.system.draggable || []) {
        this.placeOffsets[id] = { x: 0, y: 0 };
        this.placeScales[id] = 1;
      }
      for (const route of this.data.display.system.routes || []) this.edgeOffsets[route.id] = { x: 0, y: 0 };
      this.renderShell();
      this.resizeObserver.observe(this);
      if (this.getAttribute("state-src")) await this.loadViewerState();
    } catch (error) {
      this.shadowRoot.innerHTML = `<style>${NEXT_STYLES}</style><div class="error" role="alert">${escapeText(error.message)}</div>`;
    }
  }

  get checkpoints() { return this.data?.execution?.checkpoints || []; }
  get checkpoint() { return this.checkpoints[this.cursorIndex]; }
  get visualizationId() { return this.getAttribute("visualization-id") || this.data?.visualization_id || ""; }

  persistenceStatusLabel() {
    if (this.stateStatusMessage) return this.stateStatusMessage;
    return {
      loading: "Loading…",
      saving: "Saving…",
      saved: this.stateBaseMismatch ? "Saved · base changed" : `Saved · r${this.stateRevision}`,
      unsaved: this.stateBaseMismatch ? "Base changed · save" : "Unsaved changes",
      conflict: "Save conflict",
      error: "Persistence error",
      unconfigured: "",
    }[this.stateStatus] || "";
  }

  updatePersistenceControls(message = null) {
    this.stateStatusMessage = message;
    const status = this.shadowRoot.querySelector("[data-persistence-status]");
    const save = this.shadowRoot.querySelector("[data-save-state]");
    const reload = this.shadowRoot.querySelector("[data-reload-state]");
    if (status) {
      status.dataset.state = this.stateStatus;
      status.textContent = this.persistenceStatusLabel();
    }
    if (save) save.disabled = !this.stateDirty || ["loading", "saving", "conflict"].includes(this.stateStatus);
    if (reload) reload.hidden = !["conflict", "error"].includes(this.stateStatus);
  }

  layoutCheckStatusLabel() {
    if (this.layoutCheckState === "checking") return "Checking…";
    if (!this.layoutCheckReport) return "";
    const { errors } = this.layoutCheckReport.summary;
    if (errors) return `${errors} overlap${errors === 1 ? "" : "s"}`;
    return "Layout clean";
  }

  updateLayoutCheckControls() {
    const button = this.shadowRoot.querySelector("[data-check-layout]");
    const status = this.shadowRoot.querySelector("[data-layout-check-status]");
    if (button) button.disabled = this.layoutCheckState === "checking";
    if (status) {
      status.dataset.state = this.layoutCheckState;
      status.textContent = this.layoutCheckStatusLabel();
      const failures = this.layoutCheckReport?.issues.filter(issue => issue.severity === "error") || [];
      const details = failures.slice(0, 12).map(issue => {
        const format = item => `${item?.kind || "element"}:${item?.id || "unknown"} ${item?.label || ""}`.trim();
        const pair = issue.second ? ` ↔ ${format(issue.second)}` : "";
        return `${issue.projection}/${issue.checkpoint}: ${format(issue.first)}${pair}`;
      });
      status.title = details.join("\n");
      status.setAttribute("aria-label", details.length ? `${this.layoutCheckStatusLabel()}. ${details.join("; ")}` : this.layoutCheckStatusLabel());
    }
  }

  markStateDirty() {
    this.stateDirty = true;
    this.stateStatus = "unsaved";
    this.updatePersistenceControls();
    this.dispatchEvent(new CustomEvent("viewer-state-change", {
      bubbles: true,
      composed: true,
      detail: { visualization_id: this.visualizationId, dirty: true },
    }));
  }

  annotationPayload(annotation) {
    return {
      id: annotation.id,
      title: annotation.title || annotation.id,
      body: annotation.body || "",
      anchor: annotation.anchor,
      checkpoint: annotation.checkpoint || null,
      status: annotation.status === "resolved" ? "resolved" : "unresolved",
      origin: ["authored", "user", "agent"].includes(annotation.origin) ? annotation.origin : "user",
      ...(annotation.author_id ? { author_id: annotation.author_id } : {}),
    };
  }

  getAnnotations(options = {}) {
    const requestedCheckpoint = options.checkpoint || "all";
    const checkpoint = requestedCheckpoint === "current" ? this.checkpoint?.id : requestedCheckpoint;
    const status = options.status || "all";
    return this.annotations
      .filter(annotation => checkpoint === "all" || !annotation.checkpoint || annotation.checkpoint === checkpoint)
      .filter(annotation => status === "all" || annotation.status === status)
      .map(annotation => ({
        visualization_id: this.visualizationId,
        visualization_title: this.data.title,
        annotation_id: annotation.id,
        checkpoint: annotation.checkpoint || null,
        anchor: annotation.anchor,
        anchor_label: this.labelFor(annotation.anchor),
        title: annotation.title,
        body: annotation.body,
        status: annotation.status,
        origin: annotation.origin || "user",
        ...(annotation.author_id ? { author_id: annotation.author_id } : {}),
      }));
  }

  exportViewerState() {
    const baseById = new Map(this.baseAnnotations.map(annotation => [annotation.id, this.annotationPayload(annotation)]));
    const currentById = new Map(this.annotations.map(annotation => [annotation.id, this.annotationPayload(annotation)]));
    const annotations = [];
    for (const annotation of currentById.values()) {
      const base = baseById.get(annotation.id);
      if (!base || JSON.stringify(base) !== JSON.stringify(annotation)) annotations.push(annotation);
    }
    const deleted = new Set(this.deletedAnnotationIds);
    for (const identifier of baseById.keys()) if (!currentById.has(identifier)) deleted.add(identifier);
    for (const identifier of currentById.keys()) deleted.delete(identifier);
    const narrativeOverrides = {};
    for (const [checkpoint, markdown] of Object.entries(this.narrativeDrafts)) {
      if (markdown !== this.baseNarratives[checkpoint]) narrativeOverrides[checkpoint] = markdown;
    }
    return {
      version: "0.1",
      visualization_id: this.visualizationId,
      base_revision: this.data.base_revision,
      revision: this.stateRevision,
      narrative_overrides: narrativeOverrides,
      annotations,
      deleted_annotation_ids: [...deleted].sort(),
      layout: {
        shape_scale: this.shapeScale,
        place_offsets: structuredClone(this.placeOffsets),
        place_scales: structuredClone(this.placeScales),
        edge_offsets: structuredClone(this.edgeOffsets),
        collapsed_places: [],
      },
      saved_view: {
        projection: this.view,
        checkpoint: this.checkpoint?.id || null,
      },
    };
  }

  importViewerState(input, { markClean = true } = {}) {
    const state = structuredClone(input || {});
    if (state.version !== "0.1") throw new Error("Unsupported viewer-state version");
    if (state.visualization_id !== this.visualizationId) throw new Error("Viewer state belongs to a different visualization");
    this.stateRevision = Math.max(0, Number(state.revision || 0));
    this.stateBaseMismatch = Boolean(state.base_revision && state.base_revision !== this.data.base_revision);
    this.narrativeDrafts = structuredClone(this.baseNarratives);
    for (const [checkpoint, markdown] of Object.entries(state.narrative_overrides || {})) {
      if (checkpoint in this.narrativeDrafts) this.narrativeDrafts[checkpoint] = String(markdown);
    }
    this.deletedAnnotationIds = new Set(state.deleted_annotation_ids || []);
    const overlays = new Map((state.annotations || []).map(annotation => [annotation.id, this.annotationPayload(annotation)]));
    this.annotations = this.baseAnnotations
      .filter(annotation => !this.deletedAnnotationIds.has(annotation.id))
      .map(annotation => overlays.has(annotation.id)
        ? { ...structuredClone(annotation), ...overlays.get(annotation.id) }
        : structuredClone(annotation));
    for (const annotation of overlays.values()) {
      if (!this.baseAnnotations.some(base => base.id === annotation.id) && !this.deletedAnnotationIds.has(annotation.id)) {
        this.annotations.push(annotation);
      }
    }
    const layout = state.layout || {};
    this.shapeScale = clampValue(Number(layout.shape_scale || 1), .7, 1.4);
    for (const id of Object.keys(this.placeOffsets)) {
      const offset = layout.place_offsets?.[id];
      this.placeOffsets[id] = offset ? { x: Number(offset.x || 0), y: Number(offset.y || 0) } : { x: 0, y: 0 };
      this.placeScales[id] = clampValue(Number(layout.place_scales?.[id] || 1), .65, 1.75);
    }
    for (const id of Object.keys(this.edgeOffsets)) {
      const offset = layout.edge_offsets?.[id];
      this.edgeOffsets[id] = offset
        ? { x: clampValue(Number(offset.x || 0), -.45, .45), y: clampValue(Number(offset.y || 0), -.45, .45) }
        : { x: 0, y: 0 };
    }
    const savedView = state.saved_view || {};
    const allowedViews = ["ir", "compiled", "system", "timeline"];
    if (allowedViews.includes(savedView.projection)) this.view = savedView.projection;
    const checkpointIndex = this.checkpoints.findIndex(checkpoint => checkpoint.id === savedView.checkpoint);
    if (checkpointIndex >= 0) this.cursorIndex = checkpointIndex;
    this.selection = null;
    this.activeAnnotation = null;
    this.narrativeEditing = false;
    this.stateDirty = this.stateBaseMismatch || !markClean;
    this.stateStatus = this.stateDirty ? "unsaved" : "saved";
    this.stateStatusMessage = null;
    this.shadowRoot.querySelectorAll("[data-view]").forEach(button => button.setAttribute("aria-selected", String(button.dataset.view === this.view)));
    this.shadowRoot.querySelectorAll("[data-panel]").forEach(panel => { panel.hidden = panel.dataset.panel !== this.view; });
    this.render();
    this.updatePersistenceControls();
    return this.exportViewerState();
  }

  async loadViewerState() {
    const source = this.getAttribute("state-src");
    if (!source || !this.data) return null;
    this.stateStatus = "loading";
    this.updatePersistenceControls();
    try {
      const response = await fetch(source, { credentials: "same-origin" });
      if (!response.ok) throw new Error(`Unable to load viewer state (${response.status})`);
      const state = await response.json();
      this.importViewerState(state);
      this.dispatchEvent(new CustomEvent("viewer-state-load", {
        bubbles: true,
        composed: true,
        detail: { visualization_id: this.visualizationId, revision: this.stateRevision, base_mismatch: this.stateBaseMismatch },
      }));
      return state;
    } catch (error) {
      this.stateStatus = "error";
      this.updatePersistenceControls(error.message);
      this.dispatchEvent(new CustomEvent("viewer-state-error", {
        bubbles: true,
        composed: true,
        detail: { operation: "load", message: error.message },
      }));
      return null;
    }
  }

  async saveViewerState() {
    const source = this.getAttribute("state-src");
    const state = this.exportViewerState();
    if (!source) return state;
    this.stateStatus = "saving";
    this.updatePersistenceControls();
    try {
      const response = await fetch(source, {
        method: "PUT",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "If-Match": `"revision-${this.stateRevision}"`,
        },
        body: JSON.stringify(state),
      });
      if (response.status === 409 || response.status === 412) {
        this.stateStatus = "conflict";
        this.updatePersistenceControls("Reload required");
        this.dispatchEvent(new CustomEvent("viewer-state-conflict", {
          bubbles: true,
          composed: true,
          detail: { visualization_id: this.visualizationId, revision: this.stateRevision },
        }));
        return null;
      }
      if (!response.ok) throw new Error(`Unable to save viewer state (${response.status})`);
      const saved = await response.json();
      this.importViewerState(saved);
      this.dispatchEvent(new CustomEvent("viewer-state-save", {
        bubbles: true,
        composed: true,
        detail: { visualization_id: this.visualizationId, revision: this.stateRevision },
      }));
      return saved;
    } catch (error) {
      this.stateStatus = "error";
      this.updatePersistenceControls(error.message);
      this.dispatchEvent(new CustomEvent("viewer-state-error", {
        bubbles: true,
        composed: true,
        detail: { operation: "save", message: error.message },
      }));
      return null;
    }
  }

  renderShell() {
    const sourceView = this.data.source.view || {};
    const tabs = [
      ...(sourceView.show_source ? [{ id: "ir", label: "IR" }] : []),
      ...(sourceView.show_compiled ? [{ id: "compiled", label: "Compiled" }] : []),
      { id: "system", label: "System" },
      { id: "timeline", label: "Timeline" },
    ];
    if (!tabs.some(tab => tab.id === this.view)) this.view = "system";
    this.shadowRoot.innerHTML = `
      <style>${NEXT_STYLES}</style>
      <div class="root">
        <header class="head">
          <div class="heading">
            <h2 class="title">${escapeText(this.data.title)}</h2>
            <div class="subtitle">${escapeText(this.data.description || "")}</div>
          </div>
          <div class="head-actions">
            <div class="layout-check-controls">
              <output class="layout-check-status" data-layout-check-status data-state="${escapeText(this.layoutCheckState)}" aria-live="polite">${escapeText(this.layoutCheckStatusLabel())}</output>
              <button type="button" class="content-action" data-check-layout>Check layout</button>
            </div>
            ${this.getAttribute("state-src") ? `<div class="persistence-controls">
              <span class="persistence-status" data-persistence-status data-state="${escapeText(this.stateStatus)}">${this.persistenceStatusLabel()}</span>
              <button type="button" class="content-action" data-save-state ${this.stateDirty ? "" : "disabled"}>Save changes</button>
              <button type="button" class="content-action" data-reload-state ${["conflict", "error"].includes(this.stateStatus) ? "" : "hidden"}>Reload state</button>
            </div>` : ""}
            <div class="tabs" role="tablist" aria-label="Visualization views">
              ${tabs.map(tab => `<button type="button" class="tab" role="tab" data-view="${tab.id}" aria-selected="${tab.id === this.view}">${tab.label}</button>`).join("")}
            </div>
          </div>
        </header>
        <div class="workspace">
          <main class="stage">
            ${tabs.map(tab => tab.id === "ir" || tab.id === "compiled"
              ? `<pre class="panel code" data-panel="${tab.id}" ${tab.id === this.view ? "" : "hidden"}></pre>`
              : `<section class="panel canvas" data-panel="${tab.id}" ${tab.id === this.view ? "" : "hidden"}></section>`).join("")}
          </main>
          <aside class="narrative-panel" aria-label="Checkpoint narrative and annotations" data-content-panel></aside>
        </div>
        <footer class="foot">
          <div class="checkpoint" aria-live="polite">
            <div class="checkpoint-title" data-checkpoint-title></div>
            <div class="checkpoint-detail" data-checkpoint-detail></div>
          </div>
          <div class="step-controls">
            <span class="step-index" data-step-index></span>
            <button type="button" class="step-button" data-previous aria-label="Previous checkpoint">←</button>
            <button type="button" class="step-button" data-next aria-label="Next checkpoint">→</button>
          </div>
        </footer>
      </div>`;
    this.shadowRoot.querySelectorAll("[data-view]").forEach(button => button.addEventListener("click", () => this.setView(button.dataset.view)));
    this.shadowRoot.querySelector("[data-previous]").addEventListener("click", () => this.setCursor(this.cursorIndex - 1));
    this.shadowRoot.querySelector("[data-next]").addEventListener("click", () => this.setCursor(this.cursorIndex + 1));
    this.shadowRoot.querySelector("[data-check-layout]").addEventListener("click", () => this.checkDefaultLayout());
    this.shadowRoot.querySelector("[data-save-state]")?.addEventListener("click", () => this.saveViewerState());
    this.shadowRoot.querySelector("[data-reload-state]")?.addEventListener("click", () => this.loadViewerState());
    this.shadowRoot.addEventListener("keydown", event => this.handleKeydown(event));
    this.render();
  }

  setView(view) {
    this.view = view;
    this.shadowRoot.querySelectorAll("[data-view]").forEach(button => button.setAttribute("aria-selected", String(button.dataset.view === view)));
    this.shadowRoot.querySelectorAll("[data-panel]").forEach(panel => { panel.hidden = panel.dataset.panel !== view; });
    this.renderActivePanel();
    this.markStateDirty();
  }

  setCursor(index) {
    const next = clampValue(index, 0, this.checkpoints.length - 1);
    if (next === this.cursorIndex) return;
    this.cursorIndex = next;
    this.narrativeEditing = false;
    if (!this.visibleAnnotations().some(annotation => annotation.id === this.activeAnnotation)) this.activeAnnotation = null;
    this.render();
    this.dispatchEvent(new CustomEvent("cursor-change", {
      bubbles: true,
      composed: true,
      detail: { index: next, checkpoint: this.checkpoint.id, cursor: this.checkpoint.cursor },
    }));
    this.markStateDirty();
  }

  setSelection(id) {
    this.selection = this.selection === id ? null : id;
    this.render();
    this.dispatchEvent(new CustomEvent("selection-change", {
      bubbles: true,
      composed: true,
      detail: { id: this.selection },
    }));
  }

  visibleAnnotations() {
    return this.annotations.filter(annotation => !annotation.checkpoint || annotation.checkpoint === this.checkpoint.id);
  }

  annotationNumber(id) {
    const index = this.visibleAnnotations().findIndex(annotation => annotation.id === id);
    return index >= 0 ? index + 1 : 1;
  }

  emitNarrativeChange(markdown) {
    this.dispatchEvent(new CustomEvent("narrative-change", {
      bubbles: true,
      composed: true,
      detail: { checkpoint: this.checkpoint.id, markdown },
    }));
  }

  emitAnnotationChange(action, annotation) {
    this.dispatchEvent(new CustomEvent("annotation-change", {
      bubbles: true,
      composed: true,
      detail: { action, annotation: structuredClone(annotation) },
    }));
  }

  pinSelection() {
    if (!this.selection) return;
    let id;
    do {
      this.localAnnotationCounter += 1;
      id = `local.annotation.${this.localAnnotationCounter}`;
    } while (this.annotations.some(annotation => annotation.id === id));
    const annotation = {
      id,
      title: `Note on ${this.labelFor(this.selection)}`,
      body: "Add a note.",
      anchor: this.selection,
      checkpoint: this.checkpoint.id,
      status: "unresolved",
      origin: "user",
    };
    this.annotations.push(annotation);
    this.activeAnnotation = id;
    this.render();
    requestAnimationFrame(() => this.shadowRoot.querySelector(`[data-annotation-body="${CSS.escape(id)}"]`)?.select());
    this.emitAnnotationChange("create", annotation);
    this.markStateDirty();
  }

  toggleAnnotationStatus(id) {
    const annotation = this.annotations.find(item => item.id === id);
    if (!annotation) return;
    annotation.status = annotation.status === "resolved" ? "unresolved" : "resolved";
    this.render();
    this.emitAnnotationChange("status", annotation);
    this.markStateDirty();
  }

  updateAnnotation(id, field, value) {
    const annotation = this.annotations.find(item => item.id === id);
    if (!annotation || !["title", "body"].includes(field)) return;
    annotation[field] = value;
    this.emitAnnotationChange("update", annotation);
    this.markStateDirty();
  }

  deleteAnnotation(id) {
    const index = this.annotations.findIndex(annotation => annotation.id === id);
    if (index < 0) return;
    const [annotation] = this.annotations.splice(index, 1);
    if (this.baseAnnotations.some(base => base.id === id)) this.deletedAnnotationIds.add(id);
    else this.deletedAnnotationIds.delete(id);
    if (this.activeAnnotation === id) this.activeAnnotation = null;
    this.render();
    this.emitAnnotationChange("delete", annotation);
    this.markStateDirty();
  }

  openAnnotation(id) {
    this.activeAnnotation = this.activeAnnotation === id ? null : id;
    this.renderContentPanel();
    this.scheduleAnnotationPins();
    requestAnimationFrame(() => this.shadowRoot.querySelector(`[data-annotation-card="${CSS.escape(id)}"]`)?.scrollIntoView({ block: "nearest" }));
  }

  renderContentPanel() {
    const panel = this.shadowRoot.querySelector("[data-content-panel]");
    if (!panel || !this.checkpoint) return;
    const markdown = this.narrativeDrafts[this.checkpoint.id] ?? this.checkpoint.narrative ?? this.checkpoint.detail ?? "";
    const annotations = this.visibleAnnotations();
    panel.innerHTML = `
      <div class="content-heading">
        <h3>Narrative</h3>
        <button type="button" class="content-action" data-toggle-narrative>${this.narrativeEditing ? "Done" : "Edit Markdown"}</button>
      </div>
      ${this.narrativeEditing
        ? `<textarea class="narrative-input" data-narrative-input aria-label="Markdown narrative for ${escapeText(this.checkpoint.title)}">${escapeText(markdown)}</textarea>
           <div class="markdown-hint">Markdown preview</div>
           <div class="narrative-preview" data-narrative-preview>${renderMarkdown(markdown)}</div>`
        : `<div class="narrative-preview" data-narrative-preview>${renderMarkdown(markdown)}</div>`}
      <section class="annotation-section" aria-labelledby="annotation-heading">
        <div class="annotation-heading">
          <h4 id="annotation-heading">Pinned annotations</h4>
          <button type="button" class="content-action" data-pin-selection ${this.selection ? "" : "disabled"}>Pin selected</button>
        </div>
        <p class="annotation-help">Select a visual element, then pin a checkpoint-specific annotation. Resolved pins remain visible.</p>
        ${annotations.length ? `<div class="annotation-list">${annotations.map(annotation => {
          const number = this.annotationNumber(annotation.id);
          const active = annotation.id === this.activeAnnotation;
          const resolved = annotation.status === "resolved";
          return `<article class="annotation-card" data-annotation-card="${escapeText(annotation.id)}" data-active="${active}" data-status="${escapeText(annotation.status)}">
            <div class="annotation-summary">
              <button type="button" class="annotation-open" data-open-annotation="${escapeText(annotation.id)}" aria-label="${active ? "Close" : "Open"} annotation ${number}">
                <span class="annotation-number">${number}</span>
                <span class="annotation-copy">
                  <span class="annotation-title">${escapeText(annotation.title)}</span>
                  <span class="annotation-anchor">${escapeText(this.labelFor(annotation.anchor))}</span>
                </span>
              </button>
              <button type="button" class="status-switch" role="switch" aria-checked="${resolved}" data-toggle-annotation="${escapeText(annotation.id)}">${resolved ? "Resolved" : "Unresolved"}</button>
            </div>
            ${active ? `<div class="annotation-editor">
              <input class="annotation-input" data-annotation-title="${escapeText(annotation.id)}" aria-label="Annotation title" value="${escapeText(annotation.title)}">
              <textarea class="annotation-input" data-annotation-body="${escapeText(annotation.id)}" aria-label="Annotation body">${escapeText(annotation.body)}</textarea>
              <div class="annotation-editor-actions">
                <button type="button" class="content-action annotation-delete" data-delete-annotation="${escapeText(annotation.id)}">Delete annotation</button>
              </div>
            </div>` : ""}
          </article>`;
        }).join("")}</div>` : '<p class="annotation-empty">No annotations at this checkpoint.</p>'}
      </section>`;

    panel.querySelector("[data-toggle-narrative]")?.addEventListener("click", () => {
      this.narrativeEditing = !this.narrativeEditing;
      this.renderContentPanel();
      if (this.narrativeEditing) requestAnimationFrame(() => panel.querySelector("[data-narrative-input]")?.focus());
    });
    panel.querySelector("[data-narrative-input]")?.addEventListener("input", event => {
      const value = event.target.value;
      this.narrativeDrafts[this.checkpoint.id] = value;
      panel.querySelector("[data-narrative-preview]").innerHTML = renderMarkdown(value);
      this.emitNarrativeChange(value);
      this.markStateDirty();
    });
    panel.querySelector("[data-pin-selection]")?.addEventListener("click", () => this.pinSelection());
    panel.querySelectorAll("[data-open-annotation]").forEach(button => button.addEventListener("click", () => this.openAnnotation(button.dataset.openAnnotation)));
    panel.querySelectorAll("[data-toggle-annotation]").forEach(button => button.addEventListener("click", () => this.toggleAnnotationStatus(button.dataset.toggleAnnotation)));
    panel.querySelectorAll("[data-delete-annotation]").forEach(button => button.addEventListener("click", () => this.deleteAnnotation(button.dataset.deleteAnnotation)));
    panel.querySelectorAll("[data-annotation-title]").forEach(input => {
      input.addEventListener("input", () => this.updateAnnotation(input.dataset.annotationTitle, "title", input.value));
      input.addEventListener("change", () => this.renderContentPanel());
    });
    panel.querySelectorAll("[data-annotation-body]").forEach(input => {
      input.addEventListener("input", () => this.updateAnnotation(input.dataset.annotationBody, "body", input.value));
    });
  }

  resolveAnnotationTarget(surface, annotation) {
    const direct = surface.querySelector(`[data-anchor-target="${CSS.escape(annotation.anchor)}"]`);
    if (direct) return direct;
    const materialization = this.checkpoint.materializations.find(item => item.entity === annotation.anchor);
    if (materialization) {
      const target = surface.querySelector(`[data-anchor-target="${CSS.escape(materialization.id)}"]`);
      if (target) return target;
    }
    const stage = this.data.display.timeline.marks.find(mark => mark.operation === annotation.anchor || mark.flow === annotation.anchor);
    return stage ? surface.querySelector(`[data-anchor-target="${CSS.escape(stage.id)}"]`) : null;
  }

  scheduleAnnotationPins() {
    if (this.pinFrame !== null) cancelAnimationFrame(this.pinFrame);
    this.pinFrame = requestAnimationFrame(() => {
      this.pinFrame = null;
      const surface = this.view === "system"
        ? this.shadowRoot.querySelector('[data-panel="system"] .system-surface')
        : this.view === "timeline"
          ? this.shadowRoot.querySelector('[data-panel="timeline"] .timeline-surface')
          : null;
      const layer = surface?.querySelector(".pin-layer");
      if (!surface || !layer) return;
      const surfaceRect = surface.getBoundingClientRect();
      const stacks = new Map();
      layer.innerHTML = this.visibleAnnotations().map(annotation => {
        const target = this.resolveAnnotationTarget(surface, annotation);
        if (!target) return "";
        const targetRect = target.getBoundingClientRect();
        const stack = stacks.get(annotation.anchor) || 0;
        stacks.set(annotation.anchor, stack + 1);
        const left = clampValue(targetRect.right - surfaceRect.left - 11 + stack * 8, 2, Math.max(2, surfaceRect.width - 25));
        const top = clampValue(targetRect.top - surfaceRect.top - 10 + stack * 8, 2, Math.max(2, surfaceRect.height - 25));
        const number = this.annotationNumber(annotation.id);
        return `<button type="button" class="annotation-pin" style="left:${left}px;top:${top}px" data-open-pin="${escapeText(annotation.id)}" data-status="${escapeText(annotation.status)}" aria-current="${annotation.id === this.activeAnnotation}" aria-label="Open ${escapeText(annotation.status)} annotation ${number}: ${escapeText(annotation.title)}">${annotation.status === "resolved" ? "✓" : number}</button>`;
      }).join("");
      layer.querySelectorAll("[data-open-pin]").forEach(button => button.addEventListener("click", () => this.openAnnotation(button.dataset.openPin)));
    });
  }

  setShapeScale(value, emit = true) {
    if (!Number.isFinite(value)) return;
    const next = Math.round(clampValue(value, .7, 1.4) * 10) / 10;
    if (next === this.shapeScale) return;
    this.shapeScale = next;
    this.render();
    if (emit) this.emitLayoutChange();
  }

  adjustPlaceScale(id, delta) {
    if (!(id in this.placeScales)) return;
    this.placeScales[id] = Math.round(clampValue(this.placeScales[id] + delta, .65, 1.75) * 20) / 20;
    this.render();
    this.emitLayoutChange();
  }

  toggleEdgeEditMode() {
    this.edgeEditMode = !this.edgeEditMode;
    this.renderActivePanel();
  }

  resetLayout() {
    this.shapeScale = 1;
    for (const id of Object.keys(this.placeOffsets)) this.placeOffsets[id] = { x: 0, y: 0 };
    for (const id of Object.keys(this.placeScales)) this.placeScales[id] = 1;
    for (const id of Object.keys(this.edgeOffsets)) this.edgeOffsets[id] = { x: 0, y: 0 };
    this.render();
    this.emitLayoutChange();
  }

  handleKeydown(event) {
    const edgeTarget = event.target.closest?.("[data-drag-edge]");
    if (edgeTarget && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) {
      const id = edgeTarget.dataset.dragEdge;
      const delta = event.shiftKey ? .04 : .015;
      if (event.key === "ArrowLeft") this.edgeOffsets[id].x -= delta;
      if (event.key === "ArrowRight") this.edgeOffsets[id].x += delta;
      if (event.key === "ArrowUp") this.edgeOffsets[id].y -= delta;
      if (event.key === "ArrowDown") this.edgeOffsets[id].y += delta;
      this.edgeOffsets[id].x = clampValue(this.edgeOffsets[id].x, -.45, .45);
      this.edgeOffsets[id].y = clampValue(this.edgeOffsets[id].y, -.45, .45);
      event.preventDefault();
      this.render();
      requestAnimationFrame(() => this.shadowRoot.querySelector(`[data-drag-edge="${CSS.escape(id)}"]`)?.focus());
      this.emitLayoutChange();
      return;
    }
    const resizeTarget = event.target.closest?.("[data-resize-place]");
    if (resizeTarget && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) {
      const id = resizeTarget.dataset.resizePlace;
      const delta = event.shiftKey ? .1 : .05;
      this.placeScales[id] = clampValue(this.placeScales[id] + (["ArrowRight", "ArrowDown"].includes(event.key) ? delta : -delta), .65, 1.75);
      event.preventDefault();
      this.render();
      requestAnimationFrame(() => this.shadowRoot.querySelector(`[data-resize-place="${CSS.escape(id)}"]`)?.focus());
      this.emitLayoutChange();
      return;
    }
    const dragTarget = event.target.closest?.("[data-drag-place]");
    if (dragTarget && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) {
      const id = dragTarget.dataset.dragPlace;
      const delta = event.shiftKey ? .05 : .02;
      if (event.key === "ArrowLeft") this.placeOffsets[id].x -= delta;
      if (event.key === "ArrowRight") this.placeOffsets[id].x += delta;
      if (event.key === "ArrowUp") this.placeOffsets[id].y -= delta;
      if (event.key === "ArrowDown") this.placeOffsets[id].y += delta;
      event.preventDefault();
      this.render();
      requestAnimationFrame(() => this.shadowRoot.querySelector(`[data-drag-place="${CSS.escape(id)}"]`)?.focus());
      this.emitLayoutChange();
      return;
    }
    const selectable = event.target.closest?.("[data-select]");
    if (selectable && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      this.setSelection(selectable.dataset.select);
    }
  }

  beginDrag(event) {
    if (this.view !== "system") return;
    if (event.target.closest?.("[data-resize-place]")) return;
    const handle = event.target.closest?.("[data-drag-place]");
    if (!handle) return;
    const id = handle.dataset.dragPlace;
    const svg = handle.ownerSVGElement;
    const bounds = svg.getBoundingClientRect();
    const viewBox = svg.viewBox.baseVal;
    const point = pointer => ({
      x: (pointer.clientX - bounds.left) * viewBox.width / bounds.width,
      y: (pointer.clientY - bounds.top) * viewBox.height / bounds.height,
    });
    const start = point(event);
    const original = { ...this.placeOffsets[id] };
    this.dragState = { id, moved: false };

    const move = pointer => {
      const current = point(pointer);
      if (!this.dragState.moved) {
        if (Math.hypot(current.x - start.x, current.y - start.y) <= 3) return;
        this.dragState.moved = true;
      }
      this.placeOffsets[id] = {
        x: original.x + (current.x - start.x) / viewBox.width,
        y: original.y + (current.y - start.y) / viewBox.height,
      };
      pointer.preventDefault();
      this.renderActivePanel();
    };
    const finish = () => {
      const moved = this.dragState?.moved;
      this.dragState = null;
      this.ownerDocument.removeEventListener("pointermove", move);
      this.ownerDocument.removeEventListener("pointerup", finish);
      this.ownerDocument.removeEventListener("pointercancel", finish);
      if (!moved) this.placeOffsets[id] = original;
      if (moved) {
        this.render();
        this.emitLayoutChange();
      }
    };
    this.ownerDocument.addEventListener("pointermove", move, { passive: false });
    this.ownerDocument.addEventListener("pointerup", finish);
    this.ownerDocument.addEventListener("pointercancel", finish);
    event.preventDefault();
  }

  beginResize(event) {
    if (this.view !== "system") return;
    const handle = event.target.closest?.("[data-resize-place]");
    if (!handle) return;
    const id = handle.dataset.resizePlace;
    const svg = handle.ownerSVGElement;
    const bounds = svg.getBoundingClientRect();
    const viewBox = svg.viewBox.baseVal;
    const point = pointer => ({
      x: (pointer.clientX - bounds.left) * viewBox.width / bounds.width,
      y: (pointer.clientY - bounds.top) * viewBox.height / bounds.height,
    });
    const start = point(event);
    const original = this.placeScales[id];
    const box = this.profileGeometry().places[id];
    const basis = Math.max(120, (box.w + box.h) / 2);
    this.resizeState = { id };
    this.renderActivePanel();

    const move = pointer => {
      const current = point(pointer);
      const delta = ((current.x - start.x) + (current.y - start.y)) / basis;
      this.placeScales[id] = Math.round(clampValue(original + delta, .65, 1.75) * 100) / 100;
      pointer.preventDefault();
      this.renderActivePanel();
    };
    const finish = () => {
      this.resizeState = null;
      this.ownerDocument.removeEventListener("pointermove", move);
      this.ownerDocument.removeEventListener("pointerup", finish);
      this.ownerDocument.removeEventListener("pointercancel", finish);
      this.render();
      this.emitLayoutChange();
    };
    this.ownerDocument.addEventListener("pointermove", move, { passive: false });
    this.ownerDocument.addEventListener("pointerup", finish);
    this.ownerDocument.addEventListener("pointercancel", finish);
    event.stopPropagation();
    event.preventDefault();
  }

  beginEdgeDrag(event) {
    if (this.view !== "system" || !this.edgeEditMode) return;
    const handle = event.target.closest?.("[data-drag-edge]");
    if (!handle) return;
    const id = handle.dataset.dragEdge;
    const svg = handle.ownerSVGElement;
    const bounds = svg.getBoundingClientRect();
    const viewBox = svg.viewBox.baseVal;
    const point = pointer => ({
      x: (pointer.clientX - bounds.left) * viewBox.width / bounds.width,
      y: (pointer.clientY - bounds.top) * viewBox.height / bounds.height,
    });
    const start = point(event);
    const original = { ...this.edgeOffsets[id] };
    this.edgeDragState = { id };
    this.renderActivePanel();

    const move = pointer => {
      const current = point(pointer);
      this.edgeOffsets[id] = {
        x: clampValue(original.x + (current.x - start.x) / viewBox.width, -.45, .45),
        y: clampValue(original.y + (current.y - start.y) / viewBox.height, -.45, .45),
      };
      pointer.preventDefault();
      this.renderActivePanel();
    };
    const finish = () => {
      this.edgeDragState = null;
      this.ownerDocument.removeEventListener("pointermove", move);
      this.ownerDocument.removeEventListener("pointerup", finish);
      this.ownerDocument.removeEventListener("pointercancel", finish);
      this.render();
      this.emitLayoutChange();
    };
    this.ownerDocument.addEventListener("pointermove", move, { passive: false });
    this.ownerDocument.addEventListener("pointerup", finish);
    this.ownerDocument.addEventListener("pointercancel", finish);
    event.stopPropagation();
    event.preventDefault();
  }

  emitLayoutChange() {
    this.dispatchEvent(new CustomEvent("layout-change", {
      bubbles: true,
      composed: true,
      detail: {
        offsets: structuredClone(this.placeOffsets),
        place_scales: structuredClone(this.placeScales),
        edge_offsets: structuredClone(this.edgeOffsets),
        shape_scale: this.shapeScale,
      },
    }));
    this.markStateDirty();
  }

  auditCurrentLayout() {
    if (!this.data || !["system", "timeline"].includes(this.view)) {
      throw new Error("Layout audits require the System or Timeline projection");
    }
    const panel = this.shadowRoot.querySelector(`[data-panel="${this.view}"]`);
    const svg = panel?.querySelector("svg");
    if (!svg) throw new Error(`The ${this.view} projection is not rendered`);

    const issues = [];
    const describe = element => ({
      kind: element.dataset.layoutLabel || element.dataset.layoutItem || "element",
      id: element.dataset.layoutOwner || element.dataset.layoutId || element.dataset.select || "unknown",
      label: element.textContent?.trim() || element.getAttribute("aria-label") || "",
    });
    const addIssue = (code, severity, message, first, second = null) => {
      issues.push({
        code,
        severity,
        projection: this.view,
        checkpoint: this.checkpoint.id,
        message,
        first: describe(first),
        ...(second ? { second: describe(second) } : {}),
      });
    };

    const labels = [...svg.querySelectorAll("[data-layout-label]")]
      .map(element => ({ element, rect: visibleRectangle(element) }))
      .filter(item => item.rect);
    for (let firstIndex = 0; firstIndex < labels.length; firstIndex += 1) {
      for (let secondIndex = firstIndex + 1; secondIndex < labels.length; secondIndex += 1) {
        const first = labels[firstIndex];
        const second = labels[secondIndex];
        if (first.element.dataset.layoutOwner === second.element.dataset.layoutOwner) continue;
        const intersection = rectangleIntersection(first.rect, second.rect);
        if (intersection) {
          addIssue(
            "text-overlap",
            "error",
            `Text overlaps by ${intersection.width.toFixed(1)} × ${intersection.height.toFixed(1)} px`,
            first.element,
            second.element,
          );
        }
      }
    }

    const items = [...svg.querySelectorAll("[data-layout-item]")].map(element => ({
      element,
      box: element.querySelector(":scope > [data-layout-box]"),
    })).map(item => ({ ...item, rect: visibleRectangle(item.box) })).filter(item => item.rect);
    const parentByPlace = Object.fromEntries(this.data.semantic.places.map(place => [place.id, place.parent || null]));
    const isPlaceAncestor = (ancestor, descendant) => {
      let parent = parentByPlace[descendant];
      while (parent) {
        if (parent === ancestor) return true;
        parent = parentByPlace[parent];
      }
      return false;
    };
    const shouldCompareItems = (first, second) => {
      const firstKind = first.element.dataset.layoutItem;
      const secondKind = second.element.dataset.layoutItem;
      const firstId = first.element.dataset.layoutId;
      const secondId = second.element.dataset.layoutId;
      if (firstKind === "place" && secondKind === "place") {
        return !isPlaceAncestor(firstId, secondId) && !isPlaceAncestor(secondId, firstId);
      }
      if (firstKind === "timeline-mark" && secondKind === "timeline-mark") {
        return first.element.dataset.layoutLane === second.element.dataset.layoutLane
          && first.element.dataset.layoutTrack === second.element.dataset.layoutTrack;
      }
      if (firstKind === "place" || secondKind === "place") return false;
      return first.element.dataset.layoutParent
        && first.element.dataset.layoutParent === second.element.dataset.layoutParent;
    };
    for (let firstIndex = 0; firstIndex < items.length; firstIndex += 1) {
      for (let secondIndex = firstIndex + 1; secondIndex < items.length; secondIndex += 1) {
        const first = items[firstIndex];
        const second = items[secondIndex];
        if (!shouldCompareItems(first, second)) continue;
        const intersection = rectangleIntersection(first.rect, second.rect);
        if (intersection) {
          addIssue(
            "element-overlap",
            "error",
            `Elements overlap by ${intersection.width.toFixed(1)} × ${intersection.height.toFixed(1)} px`,
            first.element,
            second.element,
          );
        }
      }
    }

    for (const { element, rect } of labels) {
      const owner = element.dataset.layoutOwner;
      if (!owner) continue;
      const ownerItem = items.find(item => item.element.dataset.layoutId === owner);
      if (ownerItem && !rectangleContains(ownerItem.rect, rect, 1.5)) {
        addIssue("label-overflow", "error", "Text extends outside its owning shape", element, ownerItem.element);
      }
    }

    const edgeLabels = labels.filter(item => item.element.dataset.layoutLabel === "edge");
    for (const edgeLabel of edgeLabels) {
      for (const item of items) {
        if (rectangleIntersection(edgeLabel.rect, item.rect)) {
          addIssue("edge-label-overlap", "error", "Edge text overlaps a visual element", edgeLabel.element, item.element);
        }
      }
    }

    for (const group of svg.querySelectorAll('[data-label-fit="truncated"], [data-label-fit="hidden"]')) {
      const fit = group.dataset.labelFit;
      addIssue(
        fit === "hidden" ? "label-hidden" : "label-truncated",
        "warning",
        fit === "hidden" ? "A label is hidden at this width" : "A label is shortened at this width",
        group,
      );
    }

    const errors = issues.filter(issue => issue.severity === "error").length;
    const warnings = issues.length - errors;
    return {
      version: "0.1",
      visualization_id: this.visualizationId,
      projection: this.view,
      checkpoint: this.checkpoint.id,
      width: Math.round(this.getBoundingClientRect().width),
      shape_scale: this.shapeScale,
      status: errors ? "fail" : "pass",
      summary: { errors, warnings },
      issues,
    };
  }

  async checkDefaultLayout(options = {}) {
    if (this.layoutCheckPromise) return this.layoutCheckPromise;
    this.layoutCheckPromise = (async () => {
      const saved = {
        view: this.view,
        cursorIndex: this.cursorIndex,
        shapeScale: this.shapeScale,
        placeOffsets: structuredClone(this.placeOffsets),
        placeScales: structuredClone(this.placeScales),
        edgeOffsets: structuredClone(this.edgeOffsets),
        edgeEditMode: this.edgeEditMode,
      };
      const projections = (options.projections || ["system", "timeline"])
        .filter(projection => ["system", "timeline"].includes(projection));
      const checkpointIndexes = options.checkpoints === "current"
        ? [this.cursorIndex]
        : this.checkpoints.map((_, index) => index);
      const reports = [];
      this.layoutCheckState = "checking";
      this.updateLayoutCheckControls();
      try {
        this.shapeScale = 1;
        this.placeOffsets = Object.fromEntries(Object.keys(this.placeOffsets).map(id => [id, { x: 0, y: 0 }]));
        this.placeScales = Object.fromEntries(Object.keys(this.placeScales).map(id => [id, 1]));
        this.edgeOffsets = Object.fromEntries(Object.keys(this.edgeOffsets).map(id => [id, { x: 0, y: 0 }]));
        this.edgeEditMode = false;
        for (const projection of projections) {
          this.view = projection;
          for (const index of checkpointIndexes) {
            this.cursorIndex = index;
            this.renderActivePanel();
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
            reports.push(this.auditCurrentLayout());
          }
        }
      } finally {
        Object.assign(this, saved);
        this.render();
      }
      const allIssues = reports.flatMap(report => report.issues);
      const issueKey = issue => [
        issue.projection,
        issue.severity === "warning" ? issue.code : "overlap",
        issue.first?.kind,
        issue.first?.id,
        issue.first?.label,
        issue.second?.kind,
        issue.second?.id,
        issue.second?.label,
      ].join("|");
      const issues = [...new Map(allIssues.map(issue => [issueKey(issue), issue])).values()];
      const errors = issues.filter(issue => issue.severity === "error").length;
      const warnings = issues.length - errors;
      this.layoutCheckReport = {
        version: "0.1",
        visualization_id: this.visualizationId,
        width: Math.round(this.getBoundingClientRect().width),
        shape_scale: 1,
        status: errors ? "fail" : "pass",
        summary: { errors, warnings, checks: reports.length },
        issues,
        checks: reports,
      };
      this.layoutCheckState = this.layoutCheckReport.status;
      this.layoutCheckPromise = null;
      this.updateLayoutCheckControls();
      this.dispatchEvent(new CustomEvent("layout-check", {
        bubbles: true,
        composed: true,
        detail: this.layoutCheckReport,
      }));
      return this.layoutCheckReport;
    })().catch(error => {
      this.layoutCheckPromise = null;
      this.layoutCheckState = "fail";
      this.layoutCheckReport = {
        version: "0.1",
        visualization_id: this.visualizationId,
        status: "fail",
        summary: { errors: 1, warnings: 0, checks: 0 },
        issues: [{ code: "layout-check-error", severity: "error", message: error.message }],
        checks: [],
      };
      this.updateLayoutCheckControls();
      throw error;
    });
    return this.layoutCheckPromise;
  }

  render() {
    if (!this.data || !this.checkpoint) return;
    this.renderActivePanel();
    this.renderContentPanel();
    const selected = this.selection ? `Selected: ${this.labelFor(this.selection)}` : "";
    this.shadowRoot.querySelector("[data-checkpoint-title]").textContent = this.checkpoint.title;
    this.shadowRoot.querySelector("[data-checkpoint-detail]").textContent = selected;
    this.shadowRoot.querySelector("[data-step-index]").textContent = `${this.cursorIndex + 1} / ${this.checkpoints.length}`;
    this.shadowRoot.querySelector("[data-previous]").disabled = this.cursorIndex === 0;
    this.shadowRoot.querySelector("[data-next]").disabled = this.cursorIndex === this.checkpoints.length - 1;
  }

  renderActivePanel() {
    if (!this.data || !this.shadowRoot.querySelector(`[data-panel="${this.view}"]`)) return;
    if (this.view === "ir") {
      this.shadowRoot.querySelector('[data-panel="ir"]').textContent = JSON.stringify(this.data.source, null, 2);
    } else if (this.view === "compiled") {
      this.shadowRoot.querySelector('[data-panel="compiled"]').textContent = JSON.stringify({
        checkpoint: this.checkpoint,
        view_state: {
          selection: this.selection,
          manual_place_offsets: this.placeOffsets,
          manual_place_scales: this.placeScales,
          manual_edge_offsets: this.edgeOffsets,
          shape_scale: this.shapeScale,
        },
        system_plan: this.data.display.system,
        timeline_plan: this.data.display.timeline,
      }, null, 2);
    } else if (this.view === "system") {
      this.shadowRoot.querySelector('[data-panel="system"]').innerHTML = `<div class="system-panel">
        <div class="system-toolbar" role="toolbar" aria-label="System view layout controls">
          <span class="tool-label">Shape size</span>
          <button type="button" class="tool-button" data-scale-down aria-label="Make shapes smaller" ${this.shapeScale <= .7 ? "disabled" : ""}>−</button>
          <output class="tool-value" aria-label="Current shape size">${Math.round(this.shapeScale * 100)}%</output>
          <button type="button" class="tool-button" data-scale-up aria-label="Make shapes larger" ${this.shapeScale >= 1.4 ? "disabled" : ""}>+</button>
          <button type="button" class="tool-button" data-toggle-edge-edit aria-pressed="${this.edgeEditMode}" aria-label="Adjust edge routes">Adjust edges</button>
          <span class="tool-help">${this.edgeEditMode ? "Drag edge handles · arrow keys adjust precisely" : "Drag headers to move · drag corners to resize"}</span>
          <button type="button" class="tool-button tool-reset" data-reset-layout>Reset layout</button>
        </div>
        <div class="system-surface">${this.systemSvg()}<div class="pin-layer" aria-label="Pinned annotations"></div></div>
      </div>`;
      this.bindPanelInteractions();
    } else if (this.view === "timeline") {
      this.shadowRoot.querySelector('[data-panel="timeline"]').innerHTML = `<div class="timeline-surface">${this.timelineSvg()}<div class="pin-layer" aria-label="Pinned annotations"></div></div>`;
      this.bindPanelInteractions();
    }
    this.scheduleAnnotationPins();
  }

  bindPanelInteractions() {
    this.shadowRoot.querySelector("[data-scale-down]")?.addEventListener("click", () => this.setShapeScale(this.shapeScale - .1));
    this.shadowRoot.querySelector("[data-scale-up]")?.addEventListener("click", () => this.setShapeScale(this.shapeScale + .1));
    this.shadowRoot.querySelector("[data-toggle-edge-edit]")?.addEventListener("click", () => this.toggleEdgeEditMode());
    this.shadowRoot.querySelector("[data-reset-layout]")?.addEventListener("click", () => this.resetLayout());
    this.shadowRoot.querySelectorAll("[data-select]").forEach(target => {
      target.addEventListener("click", event => {
        event.stopPropagation();
        this.setSelection(target.dataset.select);
      });
    });
    this.shadowRoot.querySelectorAll("[data-drag-place]").forEach(target => {
      target.addEventListener("pointerdown", event => this.beginDrag(event));
    });
    this.shadowRoot.querySelectorAll("[data-resize-place]").forEach(target => {
      target.addEventListener("pointerdown", event => this.beginResize(event));
    });
    this.shadowRoot.querySelectorAll("[data-drag-edge]").forEach(target => {
      target.addEventListener("pointerdown", event => this.beginEdgeDrag(event));
    });
  }

  labelFor(id) {
    const materialization = this.checkpoint.materializations.find(item => item.id === id);
    if (materialization) return `${materialization.label} · ${materialization.place}`;
    const stage = this.data.semantic.stage_index[id];
    if (stage) return stage.label || stage.id;
    const collections = [
      this.data.semantic.places,
      this.data.semantic.resources,
      this.data.semantic.links,
      this.data.semantic.entities,
      this.data.semantic.operations,
      this.data.semantic.flows,
    ];
    for (const collection of collections) {
      const item = collection.find(candidate => candidate.id === id);
      if (item) return item.label || item.id;
    }
    return id;
  }

  profileGeometry() {
    const profileName = this.clientWidth < 620 ? "narrow" : "wide";
    const profile = this.data.display.system.geometry[profileName];
    const sourcePlaces = Object.fromEntries(Object.entries(profile.places).map(([id, box]) => [id, { ...box }]));
    const places = Object.fromEntries(Object.entries(sourcePlaces).map(([id, box]) => [id, { ...box }]));
    const children = this.data.display.system.children;
    const canvas = { ...profile.canvas };
    for (const root of this.data.display.system.draggable) {
      const base = sourcePlaces[root];
      if (!base) continue;
      const requestedX = this.placeOffsets[root]?.x || 0;
      const requestedY = this.placeOffsets[root]?.y || 0;
      const requestedScale = this.placeScales[root] || 1;
      const marginX = profileName === "narrow" ? 28 : 8;
      const marginY = profileName === "wide" ? 24 : 8;
      const scaleX = clampValue(Math.min(requestedScale, (canvas.width - marginX * 2) / base.w), .55, 1.75);
      const scaleY = clampValue(Math.min(requestedScale, (canvas.height - marginY * 2) / base.h), .55, 1.75);
      const width = base.w * scaleX;
      const height = base.h * scaleY;
      const centeredX = base.x + (base.w - width) / 2;
      const centeredY = base.y + (base.h - height) / 2;
      const targetX = clampValue(centeredX + requestedX * canvas.width, marginX, canvas.width - width - marginX);
      const targetY = clampValue(centeredY + requestedY * canvas.height, marginY, canvas.height - height - marginY);
      const pending = [root];
      while (pending.length) {
        const current = pending.pop();
        const source = sourcePlaces[current];
        if (!source) continue;
        places[current] = {
          x: targetX + (source.x - base.x) * scaleX,
          y: targetY + (source.y - base.y) * scaleY,
          w: source.w * scaleX,
          h: source.h * scaleY,
        };
        pending.push(...(children[current] || []));
      }
    }
    return { name: profileName, canvas, places };
  }

  systemSvg() {
    const plan = this.data.display.system;
    const geometry = this.profileGeometry();
    const places = geometry.places;
    const activeIds = new Set(this.checkpoint.active_stages);
    const activeStages = this.data.display.timeline.marks.filter(mark => activeIds.has(mark.id));
    const selected = this.selection;
    const materialsByPlace = {};
    for (const item of this.checkpoint.materializations) (materialsByPlace[item.place] ||= []).push(item);
    const ledgersByOwner = {};
    for (const ledger of this.checkpoint.resource_ledgers) (ledgersByOwner[ledger.owner] ||= []).push(ledger);
    const rootBoxes = plan.roots.map(id => ({ id, ...places[id] })).filter(box => Number.isFinite(box.x));
    const activeTransferGroups = activeStages
      .filter(stage => stage.kind === "transfer")
      .reduce((groups, stage) => {
        if (!groups[stage.link]) groups[stage.link] = [];
        groups[stage.link].push(stage);
        return groups;
      }, {});

    const routePaths = {};
    const routeMarkup = plan.routes.map((route, routeIndex) => {
      const from = places[route.from];
      const to = places[route.to];
      if (!from || !to) return "";
      const obstacles = rootBoxes.filter(box => box.id !== route.from && box.id !== route.to);
      const transferGroup = activeTransferGroups[route.id] || [];
      const displayLabel = transferGroup.length === 1
        ? transferGroup[0].label
        : transferGroup.length > 1
          ? `${route.label} · ${transferGroup.length} transfers`
          : route.label;
      const routed = routeConnection(from, to, obstacles, geometry.canvas, routeIndex, geometry.name, displayLabel, this.edgeOffsets[route.id]);
      routePaths[route.id] = routed;
      const active = transferGroup.length > 0;
      const isSelected = selected === route.id;
      const color = isSelected ? "var(--sv-selection)" : active ? "var(--sv-transfer)" : "var(--sv-muted)";
      const label = displayLabel.length > 32 ? `${displayLabel.slice(0, 31)}…` : displayLabel;
      const transform = routed.verticalLabel ? ` transform="rotate(-90 ${routed.label.x} ${routed.label.y})"` : "";
      return `<g data-edge-route="${escapeText(route.id)}" data-anchor-target="${escapeText(route.id)}" data-routing="${routed.external ? "external" : "direct"}">
        <title>${escapeText(displayLabel)}${active ? ` · ${escapeText(route.label)}` : ""}</title>
        <path data-edge-hit data-select="${escapeText(route.id)}" d="${routed.path}" fill="none" stroke="transparent" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
        <path data-edge-halo data-select="${escapeText(route.id)}" d="${routed.path}" fill="none" stroke="var(--sv-panel)" stroke-width="${active ? 8 : 6}" stroke-linecap="round" stroke-linejoin="round"/>
        <path data-select="${escapeText(route.id)}" id="route-${escapeText(route.id)}" d="${routed.path}" fill="none" stroke="${color}" stroke-width="${isSelected ? 4 : active ? 3 : 1.75}" stroke-linecap="round" stroke-linejoin="round" ${route.directed ? `marker-end="url(#${isSelected ? "arrow-selected" : active ? "arrow-active" : "arrow"})"` : ""}/>
        <circle data-select="${escapeText(route.id)}" cx="${routed.label.x}" cy="${routed.label.y - 4}" r="14" fill="transparent" tabindex="0" role="button" aria-label="Select link ${escapeText(route.label)}"/>
        <text class="edge-label" data-select="${escapeText(route.id)}" data-edge-label="${escapeText(route.id)}" data-layout-label="edge" data-layout-owner="${escapeText(route.id)}" x="${routed.label.x}" y="${routed.label.y}" text-anchor="middle" font-size="10" font-weight="${active ? 650 : 500}" fill="${color}"${transform}>${escapeText(label)}</text>
      </g>`;
    }).join("");

    const edgeHandleMarkup = this.edgeEditMode ? plan.routes.map(route => {
      const routed = routePaths[route.id];
      if (!routed?.handle) return "";
      const offset = this.edgeOffsets[route.id] || { x: 0, y: 0 };
      const dragging = this.edgeDragState?.id === route.id;
      return `<g data-drag-edge="${escapeText(route.id)}" data-edge-offset-x="${offset.x}" data-edge-offset-y="${offset.y}" tabindex="0" role="button" aria-label="Adjust edge ${escapeText(route.label)}. Drag or use arrow keys. Horizontal ${Math.round(offset.x * 100)}, vertical ${Math.round(offset.y * 100)}.">
        <title>Adjust ${escapeText(route.label)}</title>
        <circle cx="${routed.handle.x}" cy="${routed.handle.y}" r="${dragging ? 9 : 7}" fill="var(--sv-panel)" stroke="var(--sv-primary)" stroke-width="2"/>
        <path d="M ${routed.handle.x - 3} ${routed.handle.y} H ${routed.handle.x + 3} M ${routed.handle.x} ${routed.handle.y - 3} V ${routed.handle.y + 3}" stroke="var(--sv-primary)" stroke-width="1.5" stroke-linecap="round"/>
      </g>`;
    }).join("") : "";

    const placeMarkup = plan.places.map(place => {
      const box = places[place.id];
      if (!box) return "";
      const isRoot = plan.roots.includes(place.id);
      const active = activeStages.some(stage => stage.at === place.id);
      const rootSelected = selected === place.id;
      const stroke = rootSelected ? "var(--sv-selection)" : active ? "var(--sv-compute)" : "var(--sv-border)";
      const fill = active ? "color-mix(in srgb, var(--sv-compute) 10%, var(--sv-panel))" : isRoot ? "var(--sv-panel)" : "var(--sv-panel-soft)";
      const drag = isRoot && plan.draggable.includes(place.id);
      const fontSize = clampValue((isRoot ? 13 : 11) * this.shapeScale, 9, 17);
      const labelOffset = (isRoot ? 14 : 9) * this.shapeScale;
      const fitted = fitTimelineLabel(place.label, box.w - labelOffset - 8, fontSize);
      return `<g data-select="${escapeText(place.id)}" data-anchor-target="${escapeText(place.id)}" data-label-fit="${fitted.fit}" data-layout-item="place" data-layout-id="${escapeText(place.id)}" data-layout-parent="${escapeText(place.parent || "")}" tabindex="0" role="button" aria-label="${drag ? `Select or move ${escapeText(place.label)}. Use arrow keys for precise movement.` : `Select ${escapeText(place.label)}.`}" ${drag ? `data-drag-place="${escapeText(place.id)}" data-dragging="${this.dragState?.id === place.id}"` : ""}>
        <rect data-layout-box x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="${isRoot ? 9 : 6}" fill="${fill}" stroke="${stroke}" stroke-width="${rootSelected || active ? 2 : 1}"/>
        ${isRoot ? `<rect x="${box.x}" y="${box.y}" width="4" height="${box.h}" rx="2" fill="${place.role === "storage" ? "var(--sv-primary)" : place.role === "buffer" ? "var(--sv-compute)" : "var(--sv-selection)"}"/>` : ""}
        ${fitted.text ? `<text data-layout-label="place" data-layout-owner="${escapeText(place.id)}" x="${box.x + labelOffset}" y="${box.y + (isRoot ? 24 : 18) * this.shapeScale}" font-size="${fontSize}" font-weight="650">${escapeText(fitted.text)}</text>` : ""}
      </g>`;
    }).join("");

    const resizeMarkup = plan.draggable.map(id => {
      const box = places[id];
      if (!box) return "";
      const size = clampValue(14 * this.shapeScale, 11, 19);
      const x = box.x + box.w - size - 3;
      const y = box.y + box.h - size - 3;
      const scale = this.placeScales[id] || 1;
      return `<g data-resize-place="${escapeText(id)}" data-resizing="${this.resizeState?.id === id}" tabindex="0" role="slider" aria-label="Resize ${escapeText(id)}. Use arrow keys for precise resizing." aria-valuemin="65" aria-valuemax="175" aria-valuenow="${Math.round(scale * 100)}">
        <rect x="${x}" y="${y}" width="${size}" height="${size}" rx="3" fill="var(--sv-panel)" stroke="var(--sv-muted)"/>
        <path d="M ${x + 4} ${y + size - 4} L ${x + size - 4} ${y + 4} M ${x + 8} ${y + size - 4} L ${x + size - 4} ${y + 8}" fill="none" stroke="var(--sv-muted)" stroke-width="1.5" stroke-linecap="round"/>
      </g>`;
    }).join("");

    const chipMarkup = plan.places.map(place => {
      const box = places[place.id];
      const items = materialsByPlace[place.id] || [];
      if (!box || !items.length) return "";
      const scale = this.shapeScale;
      const chipHeight = clampValue(23 * scale, 17, 34);
      const gap = clampValue(5 * scale, 3, 8);
      const fontSize = clampValue(11 * scale, 9, 15);
      const startY = box.y + (plan.roots.includes(place.id) ? 39 : 25) * scale;
      const availableWidth = box.w - 18;
      const baseColumns = Math.max(1, Math.floor((availableWidth + gap) / (72 * scale + gap)));
      const activeCount = activeStages.filter(stage => stage.at === place.id).length;
      const hasStorageMeter = (ledgersByOwner[place.id] || []).some(ledger => ledger.kind === "storage");
      const reservedBottom = activeCount
        ? (hasStorageMeter ? 58 : 28) + Math.max(0, activeCount - 1) * 25 + 4
        : hasStorageMeter ? 37 : 4;
      const availableHeight = Math.max(chipHeight, box.y + box.h - reservedBottom - startY);
      const availableRows = Math.max(1, Math.floor((availableHeight + gap) / (chipHeight + gap)));
      const requiredColumns = Math.ceil(items.length / availableRows);
      const maximumColumns = Math.max(1, Math.floor((availableWidth + gap) / (34 * scale + gap)));
      const columns = Math.min(maximumColumns, Math.max(baseColumns, requiredColumns));
      const chipWidth = Math.min(76 * scale, (availableWidth - gap * (columns - 1)) / columns);
      return items.map((item, index) => {
        const x = box.x + 9 + (index % columns) * (chipWidth + gap);
        const y = startY + Math.floor(index / columns) * (chipHeight + gap);
        const isSelected = selected === item.id;
        const isFocused = this.checkpoint.focus.includes(item.id);
        const color = item.kind === "state" ? "var(--sv-compute)" : item.kind === "temporary-tile" ? "var(--sv-transfer)" : "var(--sv-primary)";
        const maxCharacters = Math.max(3, Math.floor((chipWidth - 12) / (fontSize * .58)));
        const label = item.label.length > maxCharacters ? `${item.label.slice(0, Math.max(2, maxCharacters - 1))}…` : item.label;
        return `<g data-select="${escapeText(item.id)}" data-anchor-target="${escapeText(item.id)}" data-layout-item="materialization" data-layout-id="${escapeText(item.id)}" data-layout-parent="${escapeText(item.place)}" tabindex="0" role="button" aria-label="Select ${escapeText(item.label)} at ${escapeText(item.place)}">
          <rect data-layout-box x="${x}" y="${y}" width="${chipWidth}" height="${chipHeight}" rx="${clampValue(5 * scale, 4, 8)}" fill="color-mix(in srgb, ${color} ${isSelected ? 24 : isFocused ? 18 : 10}%, var(--sv-panel))" stroke="${isSelected ? "var(--sv-selection)" : color}" stroke-width="${isSelected ? 2 : 1}"/>
          <text data-layout-label="materialization" data-layout-owner="${escapeText(item.id)}" x="${x + 7 * scale}" y="${y + chipHeight * .7}" font-size="${fontSize}" font-weight="${isFocused ? 650 : 500}">${escapeText(label)}</text>
        </g>`;
      }).join("");
    }).join("");

    const meterMarkup = Object.entries(ledgersByOwner).map(([owner, ledgers]) => {
      const box = places[owner];
      if (!box) return "";
      return ledgers.filter(ledger => ledger.kind === "storage").map(ledger => {
        const dimension = Object.keys(ledger.capacity)[0];
        const used = ledger.used[dimension] || 0;
        const capacity = ledger.capacity[dimension] || 1;
        const fraction = clampValue(used / capacity, 0, 1);
        const y = box.y + box.h - 13;
        const formattedUsed = dimension === "bytes" ? compactBytes(used) : `${compactNumber(used)} ${dimension}`;
        const formattedCapacity = dimension === "bytes" ? compactBytes(capacity) : `${compactNumber(capacity)} ${dimension}`;
        const isSelected = selected === ledger.resource;
        return `<g data-select="${escapeText(ledger.resource)}" data-anchor-target="${escapeText(ledger.resource)}" data-layout-item="meter" data-layout-id="${escapeText(ledger.resource)}" data-layout-parent="${escapeText(owner)}" tabindex="0" role="button" aria-label="Select resource ${escapeText(ledger.label)}">
          <rect data-layout-box x="${box.x + 7}" y="${y - 20}" width="${box.w - 14}" height="27" rx="4" fill="transparent"/>
          <text data-layout-label="meter" data-layout-owner="${escapeText(ledger.resource)}" x="${box.x + 10}" y="${y - 4}" font-size="10" font-weight="${isSelected ? 700 : 400}" fill="${isSelected ? "var(--sv-selection)" : "var(--sv-muted)"}">${formattedUsed} / ${formattedCapacity}</text>
          <rect x="${box.x + 10}" y="${y}" width="${box.w - 20}" height="4" rx="2" fill="var(--sv-border)" stroke="${isSelected ? "var(--sv-selection)" : "none"}" stroke-width="${isSelected ? 2 : 0}"/>
          <rect x="${box.x + 10}" y="${y}" width="${(box.w - 20) * fraction}" height="4" rx="2" fill="var(--sv-compute)"/>
        </g>`;
      }).join("");
    }).join("");

    const activeStageSlots = {};
    const activeMarkup = activeStages.filter(stage => stage.at && places[stage.at]).map(stage => {
      const box = places[stage.at];
      const slot = activeStageSlots[stage.at] || 0;
      activeStageSlots[stage.at] = slot + 1;
      const hasStorageMeter = (ledgersByOwner[stage.at] || []).some(ledger => ledger.kind === "storage");
      const y = box.y + box.h - (hasStorageMeter ? 58 : 28) - slot * 25;
      const fitted = fitTimelineLabel(stage.label, box.w - 26, 10);
      const isSelected = selected === stage.id;
      return `<g data-select="${escapeText(stage.id)}" data-anchor-target="${escapeText(stage.id)}" data-label-fit="${fitted.fit}" data-layout-item="stage" data-layout-id="${escapeText(stage.id)}" data-layout-parent="${escapeText(stage.at)}" tabindex="0" role="button" aria-label="Select active stage ${escapeText(stage.label)}">
        <rect data-layout-box x="${box.x + 7}" y="${y}" width="${box.w - 14}" height="21" rx="5" fill="color-mix(in srgb, var(--sv-compute) 18%, var(--sv-panel))" stroke="${isSelected ? "var(--sv-selection)" : "var(--sv-compute)"}" stroke-width="${isSelected ? 2 : 1}"/>
        ${fitted.text ? `<text data-layout-label="stage" data-layout-owner="${escapeText(stage.id)}" x="${box.x + 13}" y="${y + 15}" font-size="10" font-weight="650">${escapeText(fitted.text)}</text>` : ""}
      </g>`;
    }).join("");

    const movingMarkup = Object.entries(activeTransferGroups).map(([linkId, stages], groupIndex) => {
      if (!routePaths[linkId]) return "";
      const pathId = `moving-${groupIndex}`;
      const routed = routePaths[linkId];
      const count = stages.length;
      const radius = clampValue((count > 4 ? 5.5 : 7) * this.shapeScale, 4.5, 10);
      const circles = stages.map((stage, index) => {
        const begin = count === 1 ? "0s" : `${(-index * 1.7 / count).toFixed(2)}s`;
        const isSelected = selected === stage.id;
        return `<circle data-select="${escapeText(stage.id)}" data-anchor-target="${escapeText(stage.id)}" tabindex="0" role="button" aria-label="Select active transfer ${escapeText(stage.label)}" r="${radius}" fill="var(--sv-transfer)" stroke="${isSelected ? "var(--sv-selection)" : "var(--sv-panel)"}" stroke-width="${isSelected ? 4 : 3}">
          <title>${escapeText(stage.label)}</title>
          <animateMotion dur="1.7s" begin="${begin}" repeatCount="indefinite"><mpath href="#${pathId}"/></animateMotion>
        </circle>`;
      }).join("");
      return `<g data-active-transfer-link="${escapeText(linkId)}" data-active-transfer-count="${count}" aria-label="${count} concurrent transfers on ${escapeText(linkId)}">
        <title>${escapeText(stages.map(stage => stage.label).join("; "))}</title>
        <path id="${pathId}" d="${routed.path}" fill="none" stroke="none"/>
        ${circles}
      </g>`;
    }).join("");

    return `<svg viewBox="0 0 ${geometry.canvas.width} ${geometry.canvas.height}" role="img" aria-label="System projection at ${this.checkpoint.cursor} ${escapeText(this.data.execution.unit || "step")}">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--sv-muted)"/></marker>
        <marker id="arrow-active" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--sv-transfer)"/></marker>
        <marker id="arrow-selected" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--sv-selection)"/></marker>
      </defs>
      ${placeMarkup}
      <g class="edge-layer">${routeMarkup}</g>
      ${chipMarkup}${meterMarkup}${activeMarkup}${resizeMarkup}
      <g class="moving-layer">${movingMarkup}</g>
      <g class="edge-adjust-layer">${edgeHandleMarkup}</g>
    </svg>`;
  }

  timelineSvg() {
    const plan = this.data.display.timeline;
    const width = Math.max(320, Math.round(this.clientWidth || 720));
    const narrow = width < 620;
    const left = narrow ? 92 : 148;
    const right = 20;
    const top = 46;
    const usable = width - left - right;
    const x = value => left + usable * (value - plan.start) / Math.max(.0001, plan.end - plan.start);
    const active = new Set(this.checkpoint.active_stages);
    const colors = { transfer: "var(--sv-transfer)", compute: "var(--sv-compute)", "state-change": "var(--sv-state)", sync: "var(--sv-primary)", control: "var(--sv-state)", wait: "var(--sv-muted)" };
    let nextLaneY = top;
    const laneLayouts = plan.lanes.map((lane, index) => {
      const tracks = Math.max(1, lane.tracks || 1);
      const laneHeight = (narrow ? 27 : 21) + tracks * 31;
      const y = nextLaneY;
      nextLaneY += laneHeight;
      const fontSize = narrow ? 10 : 11;
      return { lane, index, y, laneHeight, tracks, fontSize, fitted: fitTimelineLabel(lane.label, left - 18, fontSize) };
    });
    const laneLayoutById = Object.fromEntries(laneLayouts.map(layout => [layout.lane.id, layout]));
    const timelineBottom = nextLaneY;
    const height = timelineBottom + 24;
    const laneClipDefinitions = laneLayouts.map(layout => `<clipPath id="timeline-lane-label-${layout.index}">
      <rect x="0" y="${layout.y}" width="${left - 8}" height="${layout.laneHeight - 5}"/>
    </clipPath>`).join("");
    const laneMarkup = laneLayouts.map(layout => {
      const { lane, index, y, laneHeight, fontSize, fitted } = layout;
      return `<g data-lane-label="${escapeText(lane.id)}" data-anchor-target="${escapeText(lane.id)}" data-label-fit="${fitted.fit}">
          <title>${escapeText(lane.label)}</title>
          <text data-layout-label="timeline-lane" data-layout-owner="lane:${escapeText(lane.id)}" x="${left - 10}" y="${y + laneHeight / 2 + 4}" text-anchor="end" font-size="${fontSize}" fill="var(--sv-muted)" clip-path="url(#timeline-lane-label-${index})">${escapeText(fitted.text)}</text>
        </g>
        <line x1="${left}" y1="${y + laneHeight - 5}" x2="${width - right}" y2="${y + laneHeight - 5}" stroke="var(--sv-border)"/>`;
    }).join("");
    const tickCount = narrow ? 4 : 6;
    const ticks = Array.from({ length: tickCount + 1 }, (_, index) => plan.start + (plan.end - plan.start) * index / tickCount).map(value => `<g>
      <line x1="${x(value)}" y1="${top - 8}" x2="${x(value)}" y2="${timelineBottom - 5}" stroke="color-mix(in srgb, var(--sv-border) 65%, transparent)"/>
      <text data-layout-label="timeline-tick" data-layout-owner="tick:${value}" x="${x(value)}" y="${top - 16}" text-anchor="middle" font-size="10" fill="var(--sv-muted)">${value.toFixed(1)}</text>
    </g>`).join("");
    const markLayouts = plan.marks.map((mark, markIndex) => {
      const laneLayout = laneLayoutById[mark.lane];
      if (!laneLayout) return null;
      const track = Math.max(0, Math.min(laneLayout.tracks - 1, mark.track || 0));
      const y = laneLayout.y + 8 + track * 31;
      const rawX = x(mark.start);
      const rawWidth = Math.max(0, x(mark.end) - rawX - 2);
      const minimumWidth = narrow ? 7 : 8;
      const markWidth = Math.max(minimumWidth, rawWidth);
      const markX = clampValue(rawX - Math.max(0, markWidth - rawWidth) / 2, left, width - right - markWidth);
      const isActive = active.has(mark.id);
      const isPast = mark.end <= this.checkpoint.cursor;
      const isSelected = this.selection === mark.id;
      const color = colors[mark.kind] || "var(--sv-primary)";
      const fontSize = markWidth >= 72 ? 10 : markWidth >= 42 ? 9 : 8;
      const padding = markWidth >= 42 ? 6 : 3;
      const fitted = fitTimelineLabel(mark.label, markWidth - padding * 2, fontSize);
      return { mark, markIndex, track, y, markX, markWidth, isActive, isPast, isSelected, color, fontSize, padding, fitted };
    }).filter(Boolean);
    const clipDefinitions = markLayouts.map(layout => `<clipPath id="timeline-label-${layout.markIndex}">
      <rect x="${layout.markX + 1}" y="${layout.y + 1}" width="${Math.max(0, layout.markWidth - 2)}" height="25" rx="4"/>
    </clipPath>`).join("");
    const marks = markLayouts.map(layout => {
      const { mark, markIndex, track, y, markX, markWidth, isActive, isPast, isSelected, color, fontSize, padding, fitted } = layout;
      return `<g data-select="${escapeText(mark.id)}" data-anchor-target="${escapeText(mark.id)}" data-label-fit="${fitted.fit}" data-layout-item="timeline-mark" data-layout-id="${escapeText(mark.id)}" data-layout-parent="${escapeText(mark.lane)}" data-layout-lane="${escapeText(mark.lane)}" data-layout-track="${track}" tabindex="0" role="button" aria-label="Select stage ${escapeText(mark.label)}, ${mark.start} to ${mark.end} ${escapeText(plan.unit)}">
        <title>${escapeText(mark.label)} · ${mark.start}–${mark.end} ${escapeText(plan.unit)}</title>
        <rect data-layout-box x="${markX}" y="${y}" width="${markWidth}" height="27" rx="5" fill="color-mix(in srgb, ${color} ${isActive ? 24 : isPast ? 13 : 7}%, var(--sv-panel))" stroke="${isSelected ? "var(--sv-selection)" : color}" stroke-width="${isSelected || isActive ? 2 : 1}" opacity="${isPast || isActive ? 1 : .55}"/>
        ${fitted.text ? `<text class="timeline-label" data-layout-label="timeline-mark" data-layout-owner="${escapeText(mark.id)}" x="${markX + padding}" y="${y + 17.5}" font-size="${fontSize}" font-weight="${isActive ? 650 : 500}" clip-path="url(#timeline-label-${markIndex})">${escapeText(fitted.text)}</text>` : ""}
      </g>`;
    }).join("");
    return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Resource timeline at ${this.checkpoint.cursor} ${escapeText(plan.unit)}">
      <defs>${laneClipDefinitions}${clipDefinitions}</defs>
      <text data-layout-label="timeline-title" data-layout-owner="timeline:title" x="${left}" y="18" font-size="11" fill="var(--sv-muted)">time (${escapeText(plan.unit)})</text>
      ${ticks}${laneMarkup}${marks}
      <line x1="${x(this.checkpoint.cursor)}" y1="${top - 8}" x2="${x(this.checkpoint.cursor)}" y2="${timelineBottom - 5}" stroke="var(--sv-text)" stroke-width="2"/>
      <circle cx="${x(this.checkpoint.cursor)}" cy="${top - 8}" r="4" fill="var(--sv-text)"/>
    </svg>`;
  }
}

if (!customElements.get("systems-viz-next")) customElements.define("systems-viz-next", SystemsVizNext);
