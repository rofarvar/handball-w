(() => {
  const medals = ["🥇", "🥈", "🥉"];

  const body = document.getElementById("rank-body");
  const search = document.getElementById("search");
  const teamCount = document.getElementById("team-count");
  const resultCount = document.getElementById("result-count");

  teamCount.textContent = teams.length;

  const fmt = (elo) => elo.toFixed(2);

  const rankOf = new Map();
  teams.forEach((t, i) => rankOf.set(t.name, i + 1));

  function render(filter = "") {
    const q = filter.trim().toLowerCase();
    const visible = q
      ? teams.filter((t) => t.name.toLowerCase().includes(q))
      : teams;

    body.innerHTML = "";
    visible.forEach((t) => {
      const rank = rankOf.get(t.name);
      const top = rank <= 3;
      const tr = document.createElement("tr");
      if (top) tr.className = "top-" + rank;

      const rankTd = document.createElement("td");
      rankTd.className = "rank" + (top ? " top-" + rank : "");
      rankTd.textContent = top ? medals[rank - 1] + " " + rank : rank;

      const nameTd = document.createElement("td");
      nameTd.className = "team";
      if (t.code) {
        const img = document.createElement("img");
        img.className = "flag";
        img.src = "flags/" + t.code + ".png";
        img.alt = "";
        img.loading = "lazy";
        nameTd.append(img, document.createTextNode(t.name));
      } else {
        nameTd.textContent = t.name;
      }

      const moveTd = document.createElement("td");
      moveTd.className = "move";
      if (t.move == null) {
        moveTd.textContent = "—";
      } else if (t.move > 0) {
        moveTd.textContent = "+" + t.move;
        moveTd.classList.add("up");
      } else if (t.move < 0) {
        moveTd.textContent = String(t.move);
        moveTd.classList.add("down");
      } else {
        moveTd.textContent = "0";
        moveTd.classList.add("same");
      }

      const eloTd = document.createElement("td");
      eloTd.className = "elo";
      eloTd.textContent = fmt(t.elo);

      tr.append(rankTd, nameTd, moveTd, eloTd);
      body.appendChild(tr);
    });

    resultCount.textContent = q
      ? `${visible.length} of ${teams.length} teams`
      : "";
  }

  search.addEventListener("input", () => render(search.value));
  render();
})();
