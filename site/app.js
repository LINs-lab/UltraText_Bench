"use strict";

(() => {
  const models = JSON.parse(document.getElementById("leaderboard-data").textContent).models;
  const translations = Array.from(document.querySelectorAll("[data-zh]"), (element) => ({
    element,
    en: element.innerText,
    zh: element.dataset.zh.replace(/\\n/g, "\n"),
  }));
  const head = document.getElementById("table-head");
  const body = document.getElementById("table-body");
  const search = document.getElementById("model-search");
  const view = document.getElementById("score-view");
  const count = document.getElementById("result-count");
  const toggle = document.getElementById("language-toggle");
  const copyStatus = document.getElementById("copy-status");
  const dialog = document.getElementById("image-dialog");
  const largeImage = document.getElementById("large-image");
  const imageTitle = document.getElementById("image-title");
  let language = "en";
  let access = "all";
  let sortKey = "composite";
  let descending = true;
  let activeImage = null;
  const columns = {
    model: ["Model", "模型"],
    composite: ["Composite", "综合评分"],
    text_fidelity: ["Fidelity", "保真度"],
    text_clarity: ["Clarity", "清晰度"],
    spatial_quality: ["Spatial", "空间质量"],
    scene_quality: ["Scene", "场景质量"],
    L1: ["L1", "L1"], L2: ["L2", "L2"], L3: ["L3", "L3"],
  };
  const text = (en, zh) => language === "zh" ? zh : en;
  const score = (model, key) => key.startsWith("L") ? model.levels[key][view.value] : model[key];
  const element = (tag, content, className) => {
    const result = document.createElement(tag);
    if (content !== undefined) result.textContent = content;
    if (className) result.className = className;
    return result;
  };

  function renderTable() {
    const keys = view.value === "overall"
      ? ["model", "composite", "text_fidelity", "text_clarity", "spatial_quality", "scene_quality"]
      : ["model", "L1", "L2", "L3"];
    const rank = element("th", "#");
    rank.scope = "col";
    head.replaceChildren(rank);
    for (const key of keys) {
      const th = element("th");
      th.scope = "col";
      th.setAttribute("aria-sort", key === sortKey ? (descending ? "descending" : "ascending") : "none");
      const button = element("button", columns[key][language === "zh" ? 1 : 0] + (key === sortKey ? (descending ? " ↓" : " ↑") : ""));
      button.type = "button";
      button.dataset.sort = key;
      th.append(button);
      head.append(th);
    }
    const query = search.value.trim().toLowerCase();
    const rows = models.filter(model => (access === "all" || model.access === access) && model.model.toLowerCase().includes(query));
    rows.sort((a, b) => {
      const difference = sortKey === "model"
        ? a.model.localeCompare(b.model, "en")
        : score(a, sortKey) - score(b, sortKey);
      return (descending ? -difference : difference) || a.model.localeCompare(b.model, "en");
    });
    const fragment = document.createDocumentFragment();
    rows.forEach((model, index) => {
      const row = element("tr");
      row.append(element("td", index + 1));
      const name = element("td");
      name.append(element("span", model.model, "model-name"));
      name.append(element("span", model.access === "open-weight" ? text("Open-weight", "开放权重") : text("API-only", "API 模型"), "access-label"));
      row.append(name);
      for (const key of keys.slice(1)) {
        row.append(element("td", score(model, key).toFixed(2), key === "composite" || key === "L3" ? "composite-cell" : ""));
      }
      fragment.append(row);
    });
    if (!rows.length) {
      const row = element("tr", undefined, "empty-row");
      const cell = element("td", text("No matching models. Try another name or access filter.", "没有匹配的模型，请更换名称或模型类型。"));
      cell.colSpan = keys.length + 1;
      row.append(cell);
      fragment.append(row);
    }
    body.replaceChildren(fragment);
    count.textContent = text(`${rows.length} / ${models.length} configurations`, `${rows.length} / ${models.length} 组配置`);
  }

  function updateImageTitle() {
    if (!activeImage) return;
    const title = language === "zh" ? activeImage.dataset.titleZh : activeImage.dataset.titleEn;
    imageTitle.textContent = title;
    largeImage.alt = title;
  }

  function setLanguage(next) {
    language = next;
    document.documentElement.lang = next === "zh" ? "zh-CN" : "en";
    translations.forEach(item => { item.element.textContent = item[next]; });
    toggle.textContent = text("中文 ↗", "EN ↗");
    toggle.setAttribute("aria-label", text("切换为中文", "Switch to English"));
    search.placeholder = text("Search models…", "搜索模型…");
    document.getElementById("close-image").setAttribute("aria-label", text("Close image", "关闭图片"));
    copyStatus.textContent = "";
    updateImageTitle();
    renderTable();
  }

  toggle.addEventListener("click", () => {
    setLanguage(language === "en" ? "zh" : "en");
    const url = new URL(location.href);
    if (language === "zh") url.searchParams.set("lang", "zh");
    else url.searchParams.delete("lang");
    history.replaceState(null, "", url);
  });
  search.addEventListener("input", renderTable);
  view.addEventListener("change", () => {
    sortKey = view.value === "overall" ? "composite" : "L3";
    descending = true;
    renderTable();
  });
  document.querySelectorAll("[data-access]").forEach(button => {
    button.addEventListener("click", () => {
      access = button.dataset.access;
      document.querySelectorAll("[data-access]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
      renderTable();
    });
  });
  head.addEventListener("click", event => {
    const button = event.target.closest("button[data-sort]");
    if (!button) return;
    const key = button.dataset.sort;
    descending = sortKey === key ? !descending : key !== "model";
    sortKey = key;
    renderTable();
    head.querySelector(`[data-sort="${key}"]`).focus({ preventScroll: true });
  });

  document.getElementById("copy-citation").addEventListener("click", async () => {
    const citation = document.getElementById("citation-text");
    try {
      await navigator.clipboard.writeText(citation.textContent);
      copyStatus.textContent = text("BibTeX copied.", "BibTeX 已复制。");
    } catch {
      const range = document.createRange();
      range.selectNodeContents(citation);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      copyStatus.textContent = text("BibTeX selected. Press Ctrl+C or ⌘C to copy.", "已选中 BibTeX，请按 Ctrl+C 或 ⌘C 复制。");
    }
  });

  document.querySelectorAll(".gallery-item").forEach(button => {
    button.addEventListener("click", () => {
      activeImage = button;
      largeImage.src = button.dataset.image;
      updateImageTitle();
      dialog.showModal();
    });
  });
  document.getElementById("close-image").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener("close", () => { if (activeImage) activeImage.focus({ preventScroll: true }); });
  setLanguage(new URLSearchParams(location.search).get("lang") === "zh" ? "zh" : "en");
})();
