// menü, galeri ışık kutusu, şap fiyatı hesaplayıcı
(function () {
  var btn = document.querySelector(".menu-btn"), menu = document.getElementById("menu");
  if (btn) btn.addEventListener("click", function () {
    var acik = menu.classList.toggle("acik");
    btn.setAttribute("aria-expanded", acik ? "true" : "false");
  });
  if (menu) menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") { menu.classList.remove("acik"); btn.setAttribute("aria-expanded", "false"); }
  });

  document.addEventListener("click", function (e) {
    var b = e.target.closest(".gal-ac");
    if (!b) return;
    var k = document.createElement("div");
    k.className = "isik";
    k.setAttribute("role", "dialog");
    k.setAttribute("aria-label", "Fotoğraf");
    var img = document.createElement("img");
    img.src = b.getAttribute("data-tam");
    img.alt = b.querySelector("img").alt;
    var x = document.createElement("button");
    x.type = "button"; x.setAttribute("aria-label", "Kapat"); x.textContent = "×";
    k.appendChild(img); k.appendChild(x);
    function kapat() { k.remove(); document.removeEventListener("keydown", tus); b.focus(); }
    function tus(ev) { if (ev.key === "Escape") kapat(); }
    k.addEventListener("click", function (ev) { if (ev.target !== img) kapat(); });
    document.addEventListener("keydown", tus);
    document.body.appendChild(k);
    x.focus();
  });

  var h = document.getElementById("hesap");
  if (h) {
    var g = document.getElementById("m2"), d = h.dataset;
    var f = function (n) { return Math.round(n).toLocaleString("tr-TR"); };
    var hesapla = function () {
      var m = Math.max(0, parseFloat(g.value) || 0);
      document.getElementById("h-isc").textContent = f(m * d.i0) + "–" + f(m * d.i1) + " TL";
      document.getElementById("h-mal").textContent = f(m * d.m0) + "–" + f(m * d.m1) + " TL";
    };
    g.addEventListener("input", hesapla);
  }
})();
