(function () {
  "use strict";

  const claimList = document.querySelector("#claim-list");
  const resultsLabel = document.querySelector("#results-label");
  const errorPanel = document.querySelector("#claims-error");
  const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
  const knownStatuses = new Set(["observed", "attested", "inference", "unresolved"]);

  let claims = [];
  let activeFilter = "all";

  function humanize(value) {
    return String(value).replaceAll("_", " ");
  }

  function appendTextElement(parent, tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) {
      element.className = className;
    }
    element.textContent = text;
    parent.append(element);
    return element;
  }

  function makeList(items) {
    const list = document.createElement("ul");
    items.forEach((item) => {
      appendTextElement(list, "li", "", item);
    });
    return list;
  }

  function makeRecordBlock(title, items, options = {}) {
    const block = document.createElement("section");
    block.className = options.wide ? "record-block record-block--wide" : "record-block";
    appendTextElement(block, "h4", "", title);

    if (options.evidence) {
      const list = document.createElement("ul");
      list.className = "evidence-list";
      items.forEach((reference) => {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = `./proof/evidence/${encodeURIComponent(reference)}.json`;
        link.textContent = reference;
        item.append(link);
        list.append(item);
      });
      block.append(list);
      return block;
    }

    block.append(makeList(items));
    return block;
  }

  function makeMetadata(claim) {
    const metadata = document.createElement("dl");
    metadata.className = "claim-metadata";

    [
      ["Scope", claim.scope],
      ["Claim kind", claim.claim_kind]
    ].forEach(([label, value]) => {
      const group = document.createElement("div");
      appendTextElement(group, "dt", "", label);
      appendTextElement(group, "dd", "", humanize(value));
      metadata.append(group);
    });

    return metadata;
  }

  function makeClaimCard(claim) {
    const card = document.createElement("article");
    card.className = `claim-card claim-card--${claim.status}`;
    card.dataset.status = claim.status;
    card.setAttribute("aria-labelledby", `${claim.id}-statement`);

    const index = document.createElement("div");
    index.className = "claim-card__index";
    appendTextElement(index, "p", "status-label", claim.status);
    appendTextElement(index, "p", "claim-id", `${claim.display_id} · ${claim.id}`);
    index.append(makeMetadata(claim));

    const body = document.createElement("div");
    body.className = "claim-card__body";
    const statement = appendTextElement(body, "h3", "claim-statement", claim.statement);
    statement.id = `${claim.id}-statement`;

    const records = document.createElement("div");
    records.className = "record-grid";
    records.append(
      makeRecordBlock("Evidence records", claim.evidence_refs, { evidence: true, wide: true }),
      makeRecordBlock("Limitations", claim.limitations),
      makeRecordBlock("Failure criteria", claim.failure_criteria)
    );
    body.append(records);

    card.append(index, body);
    return card;
  }

  function updateCounts() {
    const counts = claims.reduce(
      (result, claim) => {
        result.all += 1;
        result[claim.status] += 1;
        return result;
      },
      { all: 0, observed: 0, attested: 0, inference: 0, unresolved: 0 }
    );

    Object.entries(counts).forEach(([status, count]) => {
      const target = document.querySelector(`[data-count="${status}"]`);
      if (target) {
        target.textContent = String(count);
      }
    });
  }

  function applyFilter(filter) {
    activeFilter = filter;
    let visibleCount = 0;

    claimList.querySelectorAll(".claim-card").forEach((card) => {
      const show = filter === "all" || card.dataset.status === filter;
      card.hidden = !show;
      if (show) {
        visibleCount += 1;
      }
    });

    filterButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
    });

    const qualifier = filter === "all" ? "total" : filter;
    resultsLabel.textContent = `${visibleCount} ${qualifier} ${visibleCount === 1 ? "claim" : "claims"}`;
  }

  function validateClaim(claim) {
    const requiredStrings = ["id", "display_id", "status", "claim_kind", "scope", "statement"];
    const requiredLists = ["evidence_refs", "failure_criteria", "limitations"];

    const hasStrings = requiredStrings.every(
      (key) => typeof claim[key] === "string" && claim[key].trim().length > 0
    );
    const hasLists = requiredLists.every(
      (key) => Array.isArray(claim[key]) && claim[key].every((item) => typeof item === "string")
    );

    return (
      hasStrings &&
      hasLists &&
      /^C-\d{3}$/.test(claim.display_id) &&
      knownStatuses.has(claim.status)
    );
  }

  function validatePayload(payload) {
    return (
      payload &&
      payload.format === "whiteroom-claims-v1" &&
      Array.isArray(payload.claims) &&
      payload.claims.every(validateClaim)
    );
  }

  function showLoadError() {
    claimList.setAttribute("aria-busy", "false");
    resultsLabel.textContent = "Interactive claim register unavailable";
    errorPanel.hidden = false;
  }

  async function loadClaims() {
    try {
      const response = await fetch("./proof/claims.json", { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`Claim register request failed with status ${response.status}`);
      }

      const payload = await response.json();
      if (!validatePayload(payload)) {
        throw new Error("Claim register does not match the expected public format");
      }

      claims = [...payload.claims].sort((left, right) =>
        left.display_id.localeCompare(right.display_id)
      );
      const fragment = document.createDocumentFragment();
      claims.forEach((claim) => fragment.append(makeClaimCard(claim)));
      claimList.replaceChildren(fragment);
      claimList.setAttribute("aria-busy", "false");
      updateCounts();
      applyFilter(activeFilter);
    } catch (error) {
      showLoadError();
    }
  }

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => applyFilter(button.dataset.filter));
  });

  loadClaims();
})();
