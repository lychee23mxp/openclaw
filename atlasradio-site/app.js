(function () {
  const book = document.getElementById('book');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const indicator = document.getElementById('page-indicator');
  const viewFlipbookBtn = document.getElementById('view-flipbook');
  const viewMapBtn = document.getElementById('view-map');
  const flipView = document.getElementById('flipbook-view');
  const mapView = document.getElementById('map-view');

  let currentIndex = 0;
  const pages = [];

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function buildCover() {
    const page = document.createElement('div');
    page.className = 'page';
    page.innerHTML = `
      <div class="page-front cover">
        <div>
          <h1 class="cover-title">ATLAS · RADIO · CLUB</h1>
          <div class="cover-rule"></div>
          <p class="cover-sub">a flipbook atlas of the collective — one page per show, one pin per city.</p>
          <p class="cover-hint">click to begin</p>
        </div>
      </div>
      <div class="page-back cover">
        <div>
          <p class="cover-sub" style="font-style:normal;letter-spacing:0.1em;">vol. 01</p>
          <p class="cover-sub">selected transmissions ${new Date().getFullYear()}</p>
        </div>
      </div>
    `;
    return page;
  }

  function buildShowPage(show, index) {
    const page = document.createElement('div');
    page.className = 'page';
    const embedSrc = `https://w.soundcloud.com/player/?url=${encodeURIComponent(show.soundcloudUrl)}&color=%23c8553d&inverse=false&auto_play=false&show_user=true`;
    page.innerHTML = `
      <div class="page-front show-page">
        <span class="page-corner">№ ${String(index).padStart(3, '0')}</span>
        <div class="show-meta">
          <span>${escapeHtml(show.city)} · ${escapeHtml(show.country)}</span>
          <span>${escapeHtml(show.lat.toFixed(2))}, ${escapeHtml(show.lng.toFixed(2))}</span>
        </div>
        <h2 class="show-title">${escapeHtml(show.title)}</h2>
        <p class="show-host">hosted by ${escapeHtml(show.host)}</p>
        <p class="show-desc">${escapeHtml(show.description)}</p>
        <iframe class="sc-player"
          scrolling="no"
          frameborder="no"
          allow="autoplay"
          src="${embedSrc}"></iframe>
        <span class="page-num">${index}</span>
      </div>
      <div class="page-back">
        <span class="page-corner">${escapeHtml(show.country)}</span>
      </div>
    `;
    return page;
  }

  function buildBackCover() {
    const page = document.createElement('div');
    page.className = 'page';
    page.innerHTML = `
      <div class="page-front">
        <span class="page-corner">end of vol. 01</span>
      </div>
      <div class="page-back cover">
        <div>
          <h2 class="cover-title">FIN.</h2>
          <div class="cover-rule"></div>
          <p class="cover-sub">tune in &middot; <a href="https://soundcloud.com/atlasradioclub" target="_blank" rel="noopener" style="color:var(--gold);">@atlasradioclub</a></p>
        </div>
      </div>
    `;
    return page;
  }

  // Build pages: [cover, ...shows, back]
  pages.push(buildCover());
  SHOWS.forEach((show, i) => pages.push(buildShowPage(show, i + 1)));
  pages.push(buildBackCover());

  // Stack: first page on top
  pages.forEach((p, i) => {
    p.style.zIndex = String(pages.length - i);
    book.appendChild(p);
  });

  function update() {
    pages.forEach((p, i) => {
      if (i < currentIndex) p.classList.add('flipped');
      else p.classList.remove('flipped');
    });
    if (currentIndex === 0) indicator.textContent = 'cover';
    else if (currentIndex >= pages.length - 1) indicator.textContent = 'back cover';
    else indicator.textContent = `page ${currentIndex} / ${SHOWS.length}`;
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= pages.length - 1;
  }

  function goNext() {
    if (currentIndex < pages.length - 1) { currentIndex++; update(); }
  }
  function goPrev() {
    if (currentIndex > 0) { currentIndex--; update(); }
  }

  nextBtn.addEventListener('click', goNext);
  prevBtn.addEventListener('click', goPrev);

  // click on the top page to flip forward; click left edge to flip back
  book.addEventListener('click', (e) => {
    // ignore clicks inside the SoundCloud iframe / links
    if (e.target.closest('iframe, a, button')) return;
    const rect = book.getBoundingClientRect();
    const x = e.clientX - rect.left;
    if (x < rect.width * 0.3) goPrev();
    else goNext();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') goNext();
    else if (e.key === 'ArrowLeft') goPrev();
  });

  update();

  // ---- View switching ----
  function showFlipbook() {
    flipView.classList.add('active');
    mapView.classList.remove('active');
    viewFlipbookBtn.classList.add('active');
    viewMapBtn.classList.remove('active');
  }

  function showMap() {
    mapView.classList.add('active');
    flipView.classList.remove('active');
    viewMapBtn.classList.add('active');
    viewFlipbookBtn.classList.remove('active');
    initMap();
    setTimeout(() => map && map.invalidateSize(), 60);
  }

  viewFlipbookBtn.addEventListener('click', showFlipbook);
  viewMapBtn.addEventListener('click', showMap);

  // ---- Leaflet map ----
  let map = null;

  function initMap() {
    if (map) return;
    map = L.map('map', {
      worldCopyJump: true,
      scrollWheelZoom: true,
      zoomControl: true
    }).setView([20, 10], 2);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    const pinIcon = L.divIcon({
      className: 'arc-pin',
      html: '<span style="display:block;width:14px;height:14px;border-radius:50%;background:#c8553d;border:2px solid #f3e8cf;box-shadow:0 0 0 4px rgba(200,85,61,0.25);"></span>',
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    });

    SHOWS.forEach((show, i) => {
      const marker = L.marker([show.lat, show.lng], { icon: pinIcon }).addTo(map);
      const pageIndex = i + 1;
      const html = `
        <span class="popup-meta">${escapeHtml(show.city)} · ${escapeHtml(show.country)}</span>
        <span class="popup-title">${escapeHtml(show.title)}</span>
        <span>by ${escapeHtml(show.host)}</span><br>
        <button class="popup-open" data-page="${pageIndex}">open page →</button>
      `;
      marker.bindPopup(html);
      marker.on('popupopen', (ev) => {
        const btn = ev.popup.getElement().querySelector('.popup-open');
        if (btn) {
          btn.addEventListener('click', () => {
            currentIndex = pageIndex;
            update();
            showFlipbook();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          });
        }
      });
    });
  }
})();
