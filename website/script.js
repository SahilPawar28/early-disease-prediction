/**
 * Early Disease Prediction System — Project Website
 * script.js — Interactions, scroll effects, and animations
 */

/* ═══════════════════════════════════
   1. NAVBAR — scroll & mobile toggle
   ═══════════════════════════════════ */
const navbar    = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  if (window.scrollY > 40) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('mobile-open');
  const spans = hamburger.querySelectorAll('span');
  const isOpen = navLinks.classList.contains('mobile-open');
  spans[0].style.transform = isOpen ? 'translateY(7px) rotate(45deg)' : '';
  spans[1].style.opacity   = isOpen ? '0' : '1';
  spans[2].style.transform = isOpen ? 'translateY(-7px) rotate(-45deg)' : '';
});

// Close mobile menu on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('mobile-open');
    hamburger.querySelectorAll('span').forEach(s => {
      s.style.transform = '';
      s.style.opacity   = '1';
    });
  });
});

/* ═══════════════════════════════════
   2. SCROLL REVEAL
   ═══════════════════════════════════ */
const revealEls = document.querySelectorAll('.reveal');

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger sibling reveals for a cascade effect
      const siblings = [...entry.target.parentElement.children].filter(el =>
        el.classList.contains('reveal') && !el.classList.contains('visible')
      );
      const idx = siblings.indexOf(entry.target);
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, Math.min(idx * 90, 400));
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -60px 0px'
});

revealEls.forEach(el => revealObserver.observe(el));

/* ═══════════════════════════════════
   3. ANIMATED DIST BARS (on scroll)
   ═══════════════════════════════════ */
const distBarObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const fills = document.querySelectorAll('#distBars .dist-bar-fill');
      fills.forEach((fill, i) => {
        const target = fill.getAttribute('data-width');
        setTimeout(() => {
          fill.style.width = target;
        }, i * 100);
      });
      distBarObserver.disconnect();
    }
  });
}, { threshold: 0.3 });

const distSection = document.getElementById('distBars');
if (distSection) distBarObserver.observe(distSection);

/* ═══════════════════════════════════
   4. COUNTER ANIMATION (accuracy)
   ═══════════════════════════════════ */
function animateCounter(el, start, end, duration, suffix) {
  const startTime = performance.now();
  const step = (timestamp) => {
    const elapsed = timestamp - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = Math.round(start + (end - start) * eased);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const accEl = document.getElementById('acc-counter');
if (accEl) {
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(accEl, 70, 95, 1500, '%+');
        counterObserver.disconnect();
      }
    });
  }, { threshold: 0.5 });
  counterObserver.observe(accEl);
}

/* ═══════════════════════════════════
   5. SMOOTH SCROLL
   ═══════════════════════════════════ */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const navH = navbar.offsetHeight;
      const top  = target.getBoundingClientRect().top + window.scrollY - navH - 16;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ═══════════════════════════════════
   6. ACTIVE NAV HIGHLIGHT
   ═══════════════════════════════════ */
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

const navHighlightObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navAnchors.forEach(a => a.style.color = '');
      const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
      if (active && !active.classList.contains('nav-cta')) {
        active.style.color = 'var(--primary-light)';
      }
    }
  });
}, { threshold: 0.45 });

sections.forEach(s => navHighlightObserver.observe(s));

/* ═══════════════════════════════════
   7. PIPELINE STEPS — animated on scroll
   ═══════════════════════════════════ */
const pipelineSteps = document.querySelectorAll('.pipeline-step');

const pipelineObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const steps = [...pipelineSteps];
      const idx = steps.indexOf(entry.target);
      setTimeout(() => {
        entry.target.style.opacity   = '1';
        entry.target.style.transform = 'translateX(0)';
      }, idx * 80);
      pipelineObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

pipelineSteps.forEach(step => {
  step.style.opacity   = '0';
  step.style.transform = 'translateX(-30px)';
  step.style.transition = 'opacity 0.5s ease, transform 0.5s ease, background 0.3s ease';
  pipelineObserver.observe(step);
});

/* ═══════════════════════════════════
   8. HERO STATS COUNTER
   ═══════════════════════════════════ */
const statNums = document.querySelectorAll('.stat-num');
let statsAnimated = false;

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !statsAnimated) {
      statsAnimated = true;
      const targets = [7, 24, 6, 486];
      const suffixes = ['+', '', '', ''];
      statNums.forEach((el, i) => {
        const original = el.innerHTML;
        // preserve any <span> children
        animateCounter(
          { textContent: '' },
          0, targets[i], 1200, suffixes[i]
        );
        // More elegant: just do simple count
        let count = 0;
        const interval = setInterval(() => {
          count++;
          const pct = count / 30;
          const val = Math.round(targets[i] * Math.min(pct, 1));
          const span = el.querySelector('span');
          el.textContent = val + suffixes[i];
          if (span) el.appendChild(span);
          if (pct >= 1) clearInterval(interval);
        }, 30);
      });
      statsObserver.disconnect();
    }
  });
}, { threshold: 0.7 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObserver.observe(heroStats);

/* ═══════════════════════════════════
   9. TECH BADGES — hover ripple
   ═══════════════════════════════════ */
document.querySelectorAll('.tech-badge').forEach(badge => {
  badge.addEventListener('mouseenter', () => {
    badge.style.transform = 'translateY(-4px) scale(1.04)';
  });
  badge.addEventListener('mouseleave', () => {
    badge.style.transform = '';
  });
});

/* ═══════════════════════════════════
   10. DISEASE ICON ITEMS — pulse on hover
   ═══════════════════════════════════ */
document.querySelectorAll('.disease-icon-item').forEach(item => {
  item.addEventListener('mouseenter', () => {
    const emoji = item.querySelector('.di-emoji');
    if (emoji) {
      emoji.style.transform = 'scale(1.3) rotate(-5deg)';
      emoji.style.transition = 'transform 0.25s cubic-bezier(0.34,1.56,0.64,1)';
    }
  });
  item.addEventListener('mouseleave', () => {
    const emoji = item.querySelector('.di-emoji');
    if (emoji) emoji.style.transform = '';
  });
});

console.log('%c🩺 DiagnosAI — Early Disease Prediction System', 'color:#60A5FA; font-size:14px; font-weight:bold;');
console.log('%cCapstone ML Project | Built with Python, Streamlit & scikit-learn', 'color:#94A3B8; font-size:11px;');
