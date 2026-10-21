/**
 * Light Night - Controlador Principal de la Aplicación Web
 * Gestiona el estado de la sesión, la comunicación con la API FastAPI,
 * la geolocalización, el tiempo y la interactividad de la interfaz.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Estado de la aplicación
  const state = {
    latitude: 40.4168,
    longitude: -3.7038,
    placeName: 'Madrid, España',
    dateTime: null, // null = tiempo real activo
    isLive: true,
    minAltitude: 0,
    selectedConstellation: '',
    isLoading: false
  };

  // Referencias a elementos del DOM
  const elements = {
    // Header
    headerLocationText: document.getElementById('header-location-text'),
    headerTimeText: document.getElementById('header-time-text'),
    toggleSidebarBtn: document.getElementById('toggle-sidebar-btn'),
    closeSidebarBtn: document.getElementById('close-sidebar-btn'),
    sidebarPanel: document.getElementById('sidebar-panel'),

    // Ubicación
    useGpsBtn: document.getElementById('use-gps-btn'),
    citySearchForm: document.getElementById('city-search-form'),
    citySearchInput: document.getElementById('city-search-input'),
    coordLat: document.getElementById('coord-lat'),
    coordLon: document.getElementById('coord-lon'),

    // Tiempo
    datetimePicker: document.getElementById('datetime-picker'),
    setNowBtn: document.getElementById('set-now-btn'),
    stepButtons: document.querySelectorAll('.step-btn'),

    // Constelaciones
    constellationSelect: document.getElementById('constellation-select'),
    constellationListContainer: document.getElementById('constellation-list-container'),
    statsVisibleStars: document.getElementById('stats-visible-stars'),

    // Capas y controles visuales
    toggleLines: document.getElementById('toggle-lines'),
    toggleConstNames: document.getElementById('toggle-const-names'),
    toggleStarNames: document.getElementById('toggle-star-names'),
    toggleGrid: document.getElementById('toggle-grid'),
    toggleCardinals: document.getElementById('toggle-cardinals'),
    minAltitudeSlider: document.getElementById('min-altitude-slider'),
    altitudeValLabel: document.getElementById('altitude-val-label'),

    // Controles de Canvas
    zoomInBtn: document.getElementById('zoom-in-btn'),
    zoomOutBtn: document.getElementById('zoom-out-btn'),
    resetViewBtn: document.getElementById('reset-view-btn'),

    // Ficha de detalles estelares
    starDetailCard: document.getElementById('star-detail-card'),
    closeCardBtn: document.getElementById('close-card-btn'),
    cardTypeBadge: document.getElementById('card-type-badge'),
    cardTitle: document.getElementById('card-title'),
    cardSubtitle: document.getElementById('card-subtitle'),
    cardAlt: document.getElementById('card-alt'),
    cardAz: document.getElementById('card-az'),
    cardMag: document.getElementById('card-mag'),
    cardRa: document.getElementById('card-ra'),
    cardDec: document.getElementById('card-dec'),
    cardSpectral: document.getElementById('card-spectral'),
    cardLore: document.getElementById('card-lore'),

    // Contenedor de notificaciones
    toastContainer: document.getElementById('toast-container')
  };

  // Inicializar renderizador de Canvas
  const renderer = new SkyRenderer('sky-canvas', {
    onSelectStar: (star, constellation) => {
      displayStarDetails(star, constellation);
    }
  });

  // --------------------------------------------------------------------------
  // Funciones de Comunicación con la API Backend
  // --------------------------------------------------------------------------

  async function fetchSkyData() {
    if (state.isLoading) return;
    state.isLoading = true;

    try {
      const payload = {
        latitude: state.latitude,
        longitude: state.longitude,
        min_altitude: state.minAltitude,
        constellation: state.selectedConstellation || null
      };

      if (!state.isLive && state.dateTime) {
        payload.datetime_iso = state.dateTime.toISOString();
      }

      const response = await fetch('/api/sky', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Error en el servidor (${response.status})`);
      }

      const data = await response.json();
      renderer.setData(data);

      // Actualizar contadores y lista de constelaciones visibles
      elements.statsVisibleStars.textContent = data.total_visible_stars;
      renderConstellationList(data.constellations);

      // Actualizar etiqueta de hora en cabecera
      if (state.isLive) {
        elements.headerTimeText.textContent = 'En Vivo (Ahora)';
      } else if (state.dateTime) {
        elements.headerTimeText.textContent = state.dateTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' });
      }

    } catch (err) {
      console.error('Error al cargar datos astronómicos:', err);
      showToast('No se pudieron actualizar los datos del cielo. Verifica la conexión con el servidor.', 'error');
    } finally {
      state.isLoading = false;
    }
  }

  async function loadConstellationsCatalog() {
    try {
      const res = await fetch('/api/constellations');
      const data = await res.json();

      if (data.status === 'success') {
        elements.constellationSelect.innerHTML = '<option value="">✨ Todas las constelaciones</option>';
        data.constellations.forEach(c => {
          const opt = document.createElement('option');
          opt.value = c.id;
          opt.textContent = `${c.name} (${c.latin_name})`;
          elements.constellationSelect.appendChild(opt);
        });
      }
    } catch (err) {
      console.error('Error al cargar catálogo de constelaciones:', err);
    }
  }

  async function handleCitySearch(query) {
    if (!query.trim()) return;

    showToast(`Buscando coordenadas para "${query}"...`, 'info');

    try {
      const res = await fetch('/api/geocode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const result = await res.json();
      if (result.success) {
        const d = result.data;
        state.latitude = d.latitude;
        state.longitude = d.longitude;
        // Acortar nombre para la interfaz
        const shortName = d.display_name.split(',').slice(0, 2).join(', ');
        state.placeName = shortName;

        updateLocationUI();
        showToast(`Ubicación actualizada: ${shortName}`, 'success');
        fetchSkyData();
      } else {
        showToast(result.message || 'No se encontró la ubicación.', 'error');
      }
    } catch (err) {
      console.error('Error en geocodificación:', err);
      showToast('Error al conectar con el servicio de geocodificación.', 'error');
    }
  }

  async function handleBrowserGeolocation() {
    if (!navigator.geolocation) {
      showToast('Tu navegador no es compatible con geolocalización GPS.', 'error');
      return;
    }

    showToast('Solicitando permiso de ubicación al navegador...', 'info');

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        state.latitude = pos.coords.latitude;
        state.longitude = pos.coords.longitude;

        try {
          // Obtener nombre de la ciudad mediante geocodificación inversa
          const res = await fetch('/api/reverse-geocode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: state.latitude, longitude: state.longitude })
          });
          const data = await res.json();
          state.placeName = data.display_name;
        } catch {
          state.placeName = `GPS (${state.latitude.toFixed(2)}°, ${state.longitude.toFixed(2)}°)`;
        }

        updateLocationUI();
        showToast(`Ubicación GPS establecida: ${state.placeName}`, 'success');
        fetchSkyData();
      },
      (err) => {
        console.warn('Error o rechazo de geolocalización:', err);
        let msg = 'No se pudo obtener tu ubicación.';
        if (err.code === 1) {
          msg = 'Permiso de ubicación denegado. Puedes ingresar tu ciudad manualmente en el buscador.';
        } else if (err.code === 2) {
          msg = 'Posición GPS no disponible en este momento.';
        } else if (err.code === 3) {
          msg = 'Tiempo de espera de geolocalización agotado.';
        }
        showToast(msg, 'error');
      },
      { timeout: 10000, maximumAge: 60000, enableHighAccuracy: true }
    );
  }

  // --------------------------------------------------------------------------
  // Interfaz de Usuario y Renderizado de Componentes
  // --------------------------------------------------------------------------

  function updateLocationUI() {
    elements.headerLocationText.textContent = state.placeName;
    elements.coordLat.textContent = `${Math.abs(state.latitude).toFixed(3)}° ${state.latitude >= 0 ? 'N' : 'S'}`;
    elements.coordLon.textContent = `${Math.abs(state.longitude).toFixed(3)}° ${state.longitude >= 0 ? 'E' : 'O'}`;
  }

  function renderConstellationList(constellations) {
    elements.constellationListContainer.innerHTML = '';

    const visibleConsts = constellations.filter(c => c.visible_stars_count > 0);
    if (visibleConsts.length === 0) {
      elements.constellationListContainer.innerHTML = '<div style="font-size:0.78rem; color:#94a3b8; padding:0.5rem;">No hay constelaciones completas visibles en este ángulo de horizonte.</div>';
      return;
    }

    visibleConsts.forEach(c => {
      const item = document.createElement('div');
      item.className = `const-item-pill ${state.selectedConstellation === c.id ? 'active' : ''}`;
      item.innerHTML = `
        <span class="const-item-name">${c.name}</span>
        <span class="const-item-stars">${c.visible_stars_count}/${c.total_stars} ★</span>
      `;

      item.addEventListener('click', () => {
        if (state.selectedConstellation === c.id) {
          state.selectedConstellation = '';
          renderer.selectConstellation(null);
          elements.constellationSelect.value = '';
        } else {
          state.selectedConstellation = c.id;
          renderer.selectConstellation(c.id);
          elements.constellationSelect.value = c.id;
          // Si tiene estrellas visibles, enfocar y mostrar la primera
          const firstStar = c.stars.find(s => s.visible);
          if (firstStar) displayStarDetails(firstStar, c);
        }
        fetchSkyData();
      });

      elements.constellationListContainer.appendChild(item);
    });
  }

  function formatAzimuthCompass(degrees) {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.round(degrees / 22.5) % 16;
    return `${degrees.toFixed(1)}° (${directions[index]})`;
  }

  function formatRA(raHours) {
    const hours = Math.floor(raHours);
    const minutes = Math.floor((raHours - hours) * 60);
    return `${hours.toString().padStart(2, '0')}h ${minutes.toString().padStart(2, '0')}m`;
  }

  function formatDec(decDegrees) {
    const sign = decDegrees >= 0 ? '+' : '-';
    const abs = Math.abs(decDegrees);
    const deg = Math.floor(abs);
    const min = Math.floor((abs - deg) * 60);
    return `${sign}${deg.toString().padStart(2, '0')}° ${min.toString().padStart(2, '0')}'`;
  }

  function displayStarDetails(star, constellation) {
    elements.cardTypeBadge.textContent = star.tipo && star.tipo.includes('Supergigante') ? 'Supergigante' : 'Estrella';
    elements.cardTitle.textContent = star.nombre;
    elements.cardSubtitle.textContent = `Constelación de ${constellation.name || star.constelacion || 'Cielo'}`;

    elements.cardAlt.textContent = `${star.alt.toFixed(1)}° ${star.alt >= 0 ? 'sobre horizonte' : 'bajo horizonte'}`;
    elements.cardAz.textContent = formatAzimuthCompass(star.az);
    elements.cardMag.textContent = star.mag !== undefined ? star.mag.toFixed(2) : 'N/D';
    elements.cardRa.textContent = formatRA(star.ra);
    elements.cardDec.textContent = formatDec(star.dec);
    elements.cardSpectral.textContent = star.tipo || 'Desconocido';

    elements.cardLore.textContent = constellation.description || 'Punto estelar observable en la esfera celeste nocturna.';

    elements.starDetailCard.classList.remove('hidden');
  }

  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = '0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  function syncDatetimeInputWithDate(date) {
    const local = new Date(date.getTime() - (date.getTimezoneOffset() * 60000));
    elements.datetimePicker.value = local.toISOString().slice(0, 16);
  }

  // --------------------------------------------------------------------------
  // Event Listeners y Controles
  // --------------------------------------------------------------------------

  // GPS
  elements.useGpsBtn.addEventListener('click', handleBrowserGeolocation);

  // Búsqueda de Ciudad
  elements.citySearchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleCitySearch(elements.citySearchInput.value);
  });

  // Selector de fecha y hora
  elements.datetimePicker.addEventListener('change', (e) => {
    if (e.target.value) {
      state.dateTime = new Date(e.target.value);
      state.isLive = false;
      elements.setNowBtn.classList.remove('active');
      fetchSkyData();
    }
  });

  // Botón "Ahora"
  elements.setNowBtn.addEventListener('click', () => {
    state.isLive = true;
    state.dateTime = new Date();
    elements.setNowBtn.classList.add('active');
    syncDatetimeInputWithDate(state.dateTime);
    fetchSkyData();
    showToast('Sincronizado con fecha y hora actual en tiempo real.', 'info');
  });

  // Botones de paso temporal (-1h, +1h, -1d, +1d)
  elements.stepButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const stepHours = parseInt(btn.dataset.step, 10);
      const base = state.dateTime || new Date();
      state.dateTime = new Date(base.getTime() + (stepHours * 3600000));
      state.isLive = false;
      elements.setNowBtn.classList.remove('active');
      syncDatetimeInputWithDate(state.dateTime);
      fetchSkyData();
    });
  });

  // Selector de constelaciones
  elements.constellationSelect.addEventListener('change', (e) => {
    state.selectedConstellation = e.target.value;
    renderer.selectConstellation(e.target.value);
    fetchSkyData();
  });

  // Capas visuales
  elements.toggleLines.addEventListener('change', (e) => renderer.setLayer('lines', e.target.checked));
  elements.toggleConstNames.addEventListener('change', (e) => renderer.setLayer('constNames', e.target.checked));
  elements.toggleStarNames.addEventListener('change', (e) => renderer.setLayer('starNames', e.target.checked));
  elements.toggleGrid.addEventListener('change', (e) => renderer.setLayer('grid', e.target.checked));
  elements.toggleCardinals.addEventListener('change', (e) => renderer.setLayer('cardinals', e.target.checked));

  // Filtro de altitud
  elements.minAltitudeSlider.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    state.minAltitude = val;
    elements.altitudeValLabel.textContent = `${val}°`;
  });
  elements.minAltitudeSlider.addEventListener('change', () => {
    fetchSkyData();
  });

  // Controles de zoom y centrado
  elements.zoomInBtn.addEventListener('click', () => renderer.zoomIn());
  elements.zoomOutBtn.addEventListener('click', () => renderer.zoomOut());
  elements.resetViewBtn.addEventListener('click', () => {
    renderer.resetView();
    showToast('Vista restablecida al Cénit (Norte arriba).', 'info');
  });

  // Cerrar ficha de estrella
  elements.closeCardBtn.addEventListener('click', () => {
    elements.starDetailCard.classList.add('hidden');
    renderer.selectedStar = null;
  });

  // Panel lateral en dispositivos móviles
  elements.toggleSidebarBtn.addEventListener('click', () => {
    elements.sidebarPanel.classList.toggle('open');
  });
  elements.closeSidebarBtn.addEventListener('click', () => {
    elements.sidebarPanel.classList.remove('open');
  });

  // Atajos de teclado útiles
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;

    if (e.key === '+' || e.key === '=') renderer.zoomIn();
    if (e.key === '-' || e.key === '_') renderer.zoomOut();
    if (e.key === 'r' || e.key === 'R') renderer.resetView();
    if (e.key === 'Escape') elements.starDetailCard.classList.add('hidden');
  });

  // Bucle de actualización en tiempo real (cada 30 segundos si está activo)
  setInterval(() => {
    if (state.isLive) {
      state.dateTime = new Date();
      syncDatetimeInputWithDate(state.dateTime);
      fetchSkyData();
    }
  }, 30000);

  // --------------------------------------------------------------------------
  // Inicialización de la Aplicación
  // --------------------------------------------------------------------------
  const now = new Date();
  syncDatetimeInputWithDate(now);
  updateLocationUI();
  loadConstellationsCatalog();
  fetchSkyData();
});
