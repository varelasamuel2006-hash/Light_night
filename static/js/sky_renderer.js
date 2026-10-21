/**
 * Light Night - Renderizador Interactivo del Cielo Boreal y Austral
 * Maneja la proyección azimutal cenital, transformaciones geométricas (pan/zoom),
 * renderizado acelerado por Canvas 2D, detección de interacción y resaltado estelar.
 */

class SkyRenderer {
  constructor(canvasId, options = {}) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');

    // Estado de datos astronómicos
    this.snapshot = null;
    this.selectedStar = null;
    this.hoveredStar = null;
    this.selectedConstellationId = null;

    // Configuración de capas visuales
    this.layers = {
      lines: true,
      constNames: true,
      starNames: true,
      grid: true,
      cardinals: true
    };

    // Parámetros de vista (Pan & Zoom)
    this.zoom = 1.0;
    this.targetZoom = 1.0;
    this.panX = 0;
    this.panY = 0;
    this.targetPanX = 0;
    this.targetPanY = 0;

    // Estado del ratón y gestos táctiles
    this.isDragging = false;
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.lastTouchDist = null;

    // Callbacks de eventos
    this.onSelectStar = options.onSelectStar || (() => {});
    this.onSelectConstellation = options.onSelectConstellation || (() => {});

    // Inicializar listeners y bucle de render
    this.initEvents();
    this.resize();
    window.addEventListener('resize', () => this.resize());

    // Bucle de animación continuo para suavidad y destellos estelares
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.width = rect.width;
    this.height = rect.height;

    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.ctx.resetTransform();
    this.ctx.scale(dpr, dpr);

    this.baseRadius = Math.min(this.width, this.height) * 0.42;
    this.centerX = this.width / 2;
    this.centerY = this.height / 2;
  }

  setData(snapshot) {
    this.snapshot = snapshot;
  }

  setLayer(layerName, isVisible) {
    if (this.layers.hasOwnProperty(layerName)) {
      this.layers[layerName] = isVisible;
    }
  }

  selectConstellation(constId) {
    this.selectedConstellationId = constId ? constId.toLowerCase() : null;
  }

  selectStar(starName) {
    if (!this.snapshot) return;
    for (const c of this.snapshot.constellations) {
      const found = c.stars.find(s => s.nombre.toLowerCase() === starName.toLowerCase());
      if (found) {
        this.selectedStar = found;
        this.selectedConstellationId = c.id;
        this.onSelectStar(found, c);
        return;
      }
    }
  }

  resetView() {
    this.targetZoom = 1.0;
    this.targetPanX = 0;
    this.targetPanY = 0;
  }

  zoomIn() {
    this.targetZoom = Math.min(4.5, this.targetZoom * 1.3);
  }

  zoomOut() {
    this.targetZoom = Math.max(0.7, this.targetZoom / 1.3);
  }

  // Conversión de coordenadas normalizadas de proyección a coordenadas en pantalla
  skyToScreen(projX, projY) {
    const currentRadius = this.baseRadius * this.zoom;
    const x = this.centerX + this.panX + (projX * currentRadius);
    const y = this.centerY + this.panY + (projY * currentRadius);
    return { x, y };
  }

  // Conversión inversa de pantalla a proyección normalizada
  screenToSky(screenX, screenY) {
    const currentRadius = this.baseRadius * this.zoom;
    const projX = (screenX - this.centerX - this.panX) / currentRadius;
    const projY = (screenY - this.centerY - this.panY) / currentRadius;
    return { projX, projY };
  }

  initEvents() {
    // Ratón: Pan
    this.canvas.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.dragStartX = e.clientX - this.panX;
      this.dragStartY = e.clientY - this.panY;
    });

    window.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      if (this.isDragging) {
        this.targetPanX = e.clientX - this.dragStartX;
        this.targetPanY = e.clientY - this.dragStartY;
        this.panX = this.targetPanX;
        this.panY = this.targetPanY;
      } else {
        // Detección de estrella bajo el cursor (Hover)
        this.detectHover(mouseX, mouseY);
      }
    });

    window.addEventListener('mouseup', () => {
      this.isDragging = false;
    });

    // Ratón: Zoom con la rueda
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
      const newZoom = Math.max(0.7, Math.min(4.5, this.targetZoom * zoomFactor));

      // Zoom centrado hacia el cursor
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      const skyPos = this.screenToSky(mouseX, mouseY);
      this.targetZoom = newZoom;
      this.zoom = newZoom;

      const currentRadius = this.baseRadius * this.zoom;
      this.targetPanX = mouseX - this.centerX - (skyPos.projX * currentRadius);
      this.targetPanY = mouseY - this.centerY - (skyPos.projY * currentRadius);
      this.panX = this.targetPanX;
      this.panY = this.targetPanY;
    }, { passive: false });

    // Ratón: Clic para seleccionar
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      this.handleClick(mouseX, mouseY);
    });

    // Soporte táctil móvil (Pan y Pinch-to-zoom)
    this.canvas.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        this.isDragging = true;
        this.dragStartX = e.touches[0].clientX - this.panX;
        this.dragStartY = e.touches[0].clientY - this.panY;
      } else if (e.touches.length === 2) {
        this.isDragging = false;
        this.lastTouchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    });

    this.canvas.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && this.isDragging) {
        this.targetPanX = e.touches[0].clientX - this.dragStartX;
        this.targetPanY = e.touches[0].clientY - this.dragStartY;
        this.panX = this.targetPanX;
        this.panY = this.targetPanY;
      } else if (e.touches.length === 2 && this.lastTouchDist) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        const scale = dist / this.lastTouchDist;
        this.targetZoom = Math.max(0.7, Math.min(4.5, this.zoom * scale));
        this.zoom = this.targetZoom;
        this.lastTouchDist = dist;
      }
    });

    this.canvas.addEventListener('touchend', (e) => {
      if (e.touches.length === 0) {
        this.isDragging = false;
        this.lastTouchDist = null;
      }
    });
  }

  detectHover(mouseX, mouseY) {
    if (!this.snapshot) return;
    let closestStar = null;
    let minDistance = 20; // Píxeles de tolerancia

    // Buscar entre las constelaciones
    for (const c of this.snapshot.constellations) {
      for (const s of c.stars) {
        if (!s.visible) continue;
        const screenPos = this.skyToScreen(s.proj_x, s.proj_y);
        const dist = Math.hypot(screenPos.x - mouseX, screenPos.y - mouseY);
        if (dist < minDistance) {
          minDistance = dist;
          closestStar = s;
        }
      }
    }

    // Buscar entre las estrellas de referencia brillantes
    if (this.snapshot.bright_navigational_stars) {
      for (const s of this.snapshot.bright_navigational_stars) {
        const screenPos = this.skyToScreen(s.proj_x, s.proj_y);
        const dist = Math.hypot(screenPos.x - mouseX, screenPos.y - mouseY);
        if (dist < minDistance) {
          minDistance = dist;
          closestStar = s;
        }
      }
    }

    this.hoveredStar = closestStar;
    this.canvas.style.cursor = closestStar ? 'pointer' : (this.isDragging ? 'grabbing' : 'grab');
  }

  handleClick(mouseX, mouseY) {
    if (!this.snapshot) return;
    let clickedStar = null;
    let clickedConstellation = null;
    let minDistance = 24;

    for (const c of this.snapshot.constellations) {
      for (const s of c.stars) {
        if (!s.visible) continue;
        const screenPos = this.skyToScreen(s.proj_x, s.proj_y);
        const dist = Math.hypot(screenPos.x - mouseX, screenPos.y - mouseY);
        if (dist < minDistance) {
          minDistance = dist;
          clickedStar = s;
          clickedConstellation = c;
        }
      }
    }

    if (!clickedStar && this.snapshot.bright_navigational_stars) {
      for (const s of this.snapshot.bright_navigational_stars) {
        const screenPos = this.skyToScreen(s.proj_x, s.proj_y);
        const dist = Math.hypot(screenPos.x - mouseX, screenPos.y - mouseY);
        if (dist < minDistance) {
          minDistance = dist;
          clickedStar = s;
          clickedConstellation = { name: s.constelacion || 'Referencia', description: 'Estrella de navegación celeste de primera magnitud.' };
        }
      }
    }

    if (clickedStar) {
      this.selectedStar = clickedStar;
      if (clickedConstellation && clickedConstellation.id) {
        this.selectedConstellationId = clickedConstellation.id;
      }
      this.onSelectStar(clickedStar, clickedConstellation);
    }
  }

  animate(time) {
    // Suavizado cinemático
    this.zoom += (this.targetZoom - this.zoom) * 0.15;
    this.panX += (this.targetPanX - this.panX) * 0.15;
    this.panY += (this.targetPanY - this.panY) * 0.15;

    this.render(time);
    requestAnimationFrame(this.animate);
  }

  render(time) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    const currentRadius = this.baseRadius * this.zoom;
    const origin = { x: this.centerX + this.panX, y: this.centerY + this.panY };

    // 1. Dibujar Bóveda Celeste y Cuadrícula (Altitud y Azimut)
    this.drawSkyDome(origin, currentRadius);

    if (!this.snapshot) {
      this.drawLoadingMessage(origin);
      return;
    }

    // 2. Dibujar Líneas de Constelaciones
    if (this.layers.lines) {
      this.drawConstellationLines();
    }

    // 3. Dibujar Estrellas (con tamaños por magnitud y destellos)
    this.drawStars(time);

    // 4. Dibujar Nombres de Constelaciones
    if (this.layers.constNames) {
      this.drawConstellationLabels();
    }

    // 5. Dibujar Puntos Cardinales e Indicadores de Horizonte
    if (this.layers.cardinals) {
      this.drawCardinalPoints(origin, currentRadius);
    }

    // 6. Resaltar Estrella Seleccionada y Estrella Bajo Cursor
    this.drawHighlights(time);
  }

  drawSkyDome(origin, radius) {
    const ctx = this.ctx;

    // Fondo circular del domo visible
    const domeGrad = ctx.createRadialGradient(origin.x, origin.y, 0, origin.x, origin.y, radius);
    domeGrad.addColorStop(0, 'rgba(10, 18, 42, 0.7)');
    domeGrad.addColorStop(0.7, 'rgba(6, 11, 26, 0.85)');
    domeGrad.addColorStop(1, 'rgba(3, 5, 14, 0.98)');

    ctx.save();
    ctx.beginPath();
    ctx.arc(origin.x, origin.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = domeGrad;
    ctx.fill();

    // Anillo del Horizonte (Altitud = 0°)
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Cuadrícula Celeste (Círculos concéntricos de altitud 30° y 60°)
    if (this.layers.grid) {
      ctx.strokeStyle = 'rgba(99, 140, 255, 0.12)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);

      // Círculo de Altitud 60° (radio = radius * (90-60)/90 = radius / 3)
      ctx.beginPath();
      ctx.arc(origin.x, origin.y, radius * (1 / 3), 0, Math.PI * 2);
      ctx.stroke();

      // Círculo de Altitud 30° (radio = radius * (90-30)/90 = radius * 2/3)
      ctx.beginPath();
      ctx.arc(origin.x, origin.y, radius * (2 / 3), 0, Math.PI * 2);
      ctx.stroke();

      // Ejes radiales (N-S y E-W)
      ctx.beginPath();
      ctx.moveTo(origin.x, origin.y - radius);
      ctx.lineTo(origin.x, origin.y + radius);
      ctx.moveTo(origin.x - radius, origin.y);
      ctx.lineTo(origin.x + radius, origin.y);
      ctx.stroke();

      ctx.setLineDash([]);

      // Cénit (+ central)
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(origin.x - 6, origin.y);
      ctx.lineTo(origin.x + 6, origin.y);
      ctx.moveTo(origin.x, origin.y - 6);
      ctx.lineTo(origin.x, origin.y + 6);
      ctx.stroke();

      // Etiquetas de altitud en la cuadrícula
      ctx.fillStyle = 'rgba(148, 163, 184, 0.6)';
      ctx.font = '10px Space Grotesk, sans-serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'bottom';
      ctx.fillText('Alt 60°', origin.x + 4, origin.y - (radius * 1 / 3) - 2);
      ctx.fillText('Alt 30°', origin.x + 4, origin.y - (radius * 2 / 3) - 2);
      ctx.fillText('Cénit 90°', origin.x + 8, origin.y + 12);
    }

    ctx.restore();
  }

  drawCardinalPoints(origin, radius) {
    const ctx = this.ctx;
    ctx.save();
    ctx.font = 'bold 13px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    const points = [
      { label: 'N', x: origin.x, y: origin.y - radius - 14, color: '#38bdf8' },
      { label: 'S', x: origin.x, y: origin.y + radius + 14, color: '#f1f5f9' },
      { label: 'E', x: origin.x - radius - 14, y: origin.y, color: '#f1f5f9' },
      { label: 'W', x: origin.x + radius + 14, y: origin.y, color: '#f1f5f9' }
    ];

    for (const p of points) {
      // Fondo sutil para la letra
      ctx.fillStyle = 'rgba(7, 9, 19, 0.8)';
      ctx.beginPath();
      ctx.arc(p.x, p.y, 11, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
      ctx.stroke();

      ctx.fillStyle = p.color;
      ctx.fillText(p.label, p.x, p.y);
    }
    ctx.restore();
  }

  drawConstellationLines() {
    const ctx = this.ctx;
    ctx.save();

    for (const c of this.snapshot.constellations) {
      const isSelected = this.selectedConstellationId === c.id;

      if (isSelected) {
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.2;
        ctx.shadowColor = 'rgba(56, 189, 248, 0.8)';
        ctx.shadowBlur = 10;
      } else {
        ctx.strokeStyle = 'rgba(99, 140, 255, 0.38)';
        ctx.lineWidth = 1.2;
        ctx.shadowBlur = 0;
      }

      ctx.beginPath();
      for (const line of c.lines) {
        const p1 = this.skyToScreen(line.origen_pos.x, line.origen_pos.y);
        const p2 = this.skyToScreen(line.destino_pos.x, line.destino_pos.y);

        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
      }
      ctx.stroke();
    }

    ctx.restore();
  }

  drawStars(time) {
    const ctx = this.ctx;
    ctx.save();

    const allStars = [];
    for (const c of this.snapshot.constellations) {
      for (const s of c.stars) {
        if (s.visible) allStars.push(s);
      }
    }
    if (this.snapshot.bright_navigational_stars) {
      for (const s of this.snapshot.bright_navigational_stars) {
        if (s.visible) allStars.push(s);
      }
    }

    // Dibujar cada estrella
    for (const star of allStars) {
      const pos = this.skyToScreen(star.proj_x, star.proj_y);

      // Calcular radio según magnitud (mag menor = más brillo)
      // Escala: mag -1.5 -> radio 5.5px, mag 4 -> radio 2px
      const baseSize = Math.max(2.0, 5.0 - (star.mag * 0.7));
      // Destello sutil basado en tiempo
      const twinkle = Math.sin((time * 0.003) + (star.ra * 10)) * 0.3 + 1;
      const size = baseSize * twinkle;

      // Halo resplandeciente para estrellas brillantes (mag < 2.5)
      if (star.mag < 2.5) {
        const haloGrad = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, size * 3.5);
        haloGrad.addColorStop(0, star.color || 'rgba(255, 255, 255, 0.8)');
        haloGrad.addColorStop(0.4, 'rgba(56, 189, 248, 0.25)');
        haloGrad.addColorStop(1, 'transparent');

        ctx.fillStyle = haloGrad;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, size * 3.5, 0, Math.PI * 2);
        ctx.fill();
      }

      // Núcleo estelar
      ctx.fillStyle = star.color || '#ffffff';
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2);
      ctx.fill();

      // Nombres de estrellas
      if (this.layers.starNames && (star.mag < 2.8 || this.selectedConstellationId)) {
        ctx.font = '11px Outfit, sans-serif';
        ctx.fillStyle = 'rgba(241, 245, 249, 0.82)';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText(star.nombre, pos.x + size + 4, pos.y - 1);
      }
    }

    ctx.restore();
  }

  drawConstellationLabels() {
    const ctx = this.ctx;
    ctx.save();
    ctx.font = 'bold 12px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (const c of this.snapshot.constellations) {
      if (c.visible_stars_count === 0) continue;

      // Calcular baricentro de las estrellas visibles
      let avgX = 0;
      let avgY = 0;
      let count = 0;

      for (const s of c.stars) {
        if (s.visible) {
          avgX += s.proj_x;
          avgY += s.proj_y;
          count++;
        }
      }

      if (count > 0) {
        avgX /= count;
        avgY /= count;
        const pos = this.skyToScreen(avgX, avgY);

        const isSelected = this.selectedConstellationId === c.id;
        ctx.fillStyle = isSelected ? '#38bdf8' : 'rgba(148, 163, 184, 0.85)';

        // Etiqueta de la constelación
        ctx.fillText(c.name.toUpperCase(), pos.x, pos.y - 14);
      }
    }
    ctx.restore();
  }

  drawHighlights(time) {
    const ctx = this.ctx;
    ctx.save();

    // Resaltado de estrella seleccionada
    if (this.selectedStar && this.selectedStar.visible) {
      const pos = this.skyToScreen(this.selectedStar.proj_x, this.selectedStar.proj_y);
      const pulse = Math.sin(time * 0.006) * 3 + 14;

      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.shadowColor = 'rgba(56, 189, 248, 0.9)';
      ctx.shadowBlur = 12;

      ctx.beginPath();
      ctx.arc(pos.x, pos.y, pulse, 0, Math.PI * 2);
      ctx.stroke();

      // Marcadores en cruz
      ctx.beginPath();
      ctx.moveTo(pos.x - pulse - 4, pos.y);
      ctx.lineTo(pos.x - pulse + 2, pos.y);
      ctx.moveTo(pos.x + pulse - 2, pos.y);
      ctx.lineTo(pos.x + pulse + 4, pos.y);
      ctx.moveTo(pos.x, pos.y - pulse - 4);
      ctx.lineTo(pos.x, pos.y - pulse + 2);
      ctx.moveTo(pos.x, pos.y + pulse - 2);
      ctx.lineTo(pos.x, pos.y + pulse + 4);
      ctx.stroke();
    }

    // Resaltado de estrella bajo cursor (Hover)
    if (this.hoveredStar && this.hoveredStar.visible && this.hoveredStar !== this.selectedStar) {
      const pos = this.skyToScreen(this.hoveredStar.proj_x, this.hoveredStar.proj_y);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 12, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawLoadingMessage(origin) {
    const ctx = this.ctx;
    ctx.save();
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = '14px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Calculando coordenadas celestes con Skyfield...', origin.x, origin.y);
    ctx.restore();
  }
}
