// Lazy-loading enhancements: native attribute + IntersectionObserver fallback
document.addEventListener("DOMContentLoaded", () => {
  // Prefer native lazy loading where supported by setting attributes
  document.querySelectorAll("img").forEach((img) => {
    if (!img.hasAttribute("loading")) img.setAttribute("loading", "lazy");
    if (!img.hasAttribute("decoding")) img.setAttribute("decoding", "async");
  });

  // Support images/backgrounds that use data-src, data-srcset or data-bg attributes
  const lazyTargets = document.querySelectorAll(
    "img[data-src], img[data-srcset], [data-bg]",
  );

  if ("IntersectionObserver" in window && lazyTargets.length) {
    const lazyObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;

          if (el.tagName === "IMG") {
            if (el.dataset.src) el.src = el.dataset.src;
            if (el.dataset.srcset) el.srcset = el.dataset.srcset;
            el.removeAttribute("data-src");
            el.removeAttribute("data-srcset");
          } else if (el.dataset && el.dataset.bg) {
            el.style.backgroundImage = `url('${el.dataset.bg}')`;
            el.removeAttribute("data-bg");
          }

          obs.unobserve(el);
        });
      },
      {
        rootMargin: "200px 0px",
        threshold: 0.01,
      },
    );

    lazyTargets.forEach((t) => lazyObserver.observe(t));
  } else if (lazyTargets.length) {
    // Fallback: eagerly load all lazy targets
    lazyTargets.forEach((el) => {
      if (el.tagName === "IMG") {
        if (el.dataset.src) el.src = el.dataset.src;
        if (el.dataset.srcset) el.srcset = el.dataset.srcset;
      } else if (el.dataset && el.dataset.bg) {
        el.style.backgroundImage = `url('${el.dataset.bg}')`;
      }
    });
  }
});
