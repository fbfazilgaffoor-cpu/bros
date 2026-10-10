/* ═══════════════════════════════════════════════════════════
   LESSON 2 — Generating Sneaker Concepts with AI
   GOAL: Send form data to /generate and display the concept.
   ═══════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const generateBtn  = document.getElementById('generateBtn');
  const formError    = document.getElementById('formError');
  const emptyState   = document.getElementById('emptyState');
  const loadingState = document.getElementById('loadingState');
  const loaderText   = document.getElementById('loaderText');
  const result       = document.getElementById('result');

  // Chip selection (from Lesson 1)
  document.querySelectorAll('.chip-group').forEach(group => {
    const hiddenInput = document.getElementById(group.dataset.field);
    group.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', () => {
        group.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        if (hiddenInput) hiddenInput.value = chip.dataset.value;
      });
    });
  });

  // Color sync (from Lesson 1)
  function syncColor(pid, tid) {
    const p = document.getElementById(pid), t = document.getElementById(tid);
    if (!p || !t) return;
    p.addEventListener('input', () => t.value = p.value);
    t.addEventListener('input', () => { if (/^#[0-9A-Fa-f]{6}$/.test(t.value)) p.value = t.value; });
  }
  syncColor('primary_color', 'primary_color_text');
  syncColor('accent_color',  'accent_color_text');

  const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');


  // TODO 1: Write collectPrefs()
  // Return object with: style, material, occasion,
  // primary_color, accent_color, inspiration


  // TODO 2: Write renderConcept(c)
  // Populate: resultName, resultTagline, resultDesc,
  // resultPrice, resultAudience, resultTags,
  // materialsList (<li> items), featuresList (<li> items), soleText


  // TODO 3: Wire Generate button
  // On click: disable button, show loadingState
  // POST to /generate with collectPrefs() as JSON body
  // On success: call renderConcept, hide loadingState, show result
  // On error: show formError
  // Re-enable button in finally

})();
