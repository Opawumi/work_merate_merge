document.addEventListener("DOMContentLoaded", () => {
  // 1. The Modal HTML String (Added style="display: none;" to the main wrapper)
  const modalHTML = `
    <div id="requestDemoModal" class="demo-modal-overlay" aria-hidden="true" style="display: none;">
      <div class="demo-modal-box" role="dialog" aria-modal="true" aria-labelledby="requestDemoTitle">
        <button class="demo-modal-close" id="closeRequestDemo" aria-label="Close">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <h2 class="demo-modal-title" id="requestDemoTitle">Get a Free Demo of WorkMerate</h2>
        <form class="demo-modal-form" onsubmit="return false;">
          <div class="demo-form-row">
            <input type="text" class="demo-input" placeholder="First Name" required />
            <input type="text" class="demo-input" placeholder="Last Name" required />
          </div>
          <div class="demo-form-row">
            <input type="email" class="demo-input" placeholder="Email Address" required />
            <input type="tel" class="demo-input" placeholder="Phone Number" required />
          </div>
          <input type="url" class="demo-input demo-input-full" placeholder="Website URL" />
          <div class="demo-select-wrapper">
            <select class="demo-select">
              <option value="" disabled selected>How many employees work there?</option>
              <option value="1-10">1 – 10</option>
              <option value="11-50">11 – 50</option>
              <option value="51-200">51 – 200</option>
              <option value="201-500">201 – 500</option>
              <option value="501+">501+</option>
            </select>
            <svg class="demo-select-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
          <label class="demo-consent-label">
            <input type="checkbox" class="demo-checkbox" checked />
            <span class="demo-consent-text">
              By clicking "Get your free demo", you agree to <strong>WorkMerate</strong> contacting you with marketing-related emails or by telephone. You may unsubscribe from these communications at any time. For information on how to unsubscribe, as well as our privacy practices and commitment to protecting your privacy, please review our <a href="privacy.html" class="demo-privacy-link">Privacy Policy</a>
            </span>
          </label>
          <button type="submit" class="demo-submit-btn">Get demo</button>
        </form>
      </div>
    </div>
  `;

  // 2. Inject HTML into the body if it doesn't already exist
  if (!document.getElementById("requestDemoModal")) {
    document.body.insertAdjacentHTML("beforeend", modalHTML);
  }

  // 3. Select DOM Elements
  const modal = document.getElementById("requestDemoModal");
  const closeBtn = document.getElementById("closeRequestDemo");

  // 4. Open and Close Functions (Updated to force inline display styles)
  const openModal = () => {
    modal.setAttribute("aria-hidden", "false");
    modal.style.display = "flex"; // Forces the modal to show
    document.body.style.overflow = "hidden"; // Prevent background scrolling
  };

  const closeModal = () => {
    modal.setAttribute("aria-hidden", "true");
    modal.style.display = "none"; // Forces the modal to hide

    // Ensure we only restore overflow if other modals aren't open
    const exploreModal = document.getElementById("exploreModulesModal");
    if (!exploreModal || exploreModal.getAttribute("aria-hidden") === "true") {
      document.body.style.overflow = "";
    }
  };

  // Expose to window in case you still want to use inline `onclick="openRequestDemoModal()"`
  window.openRequestDemoModal = openModal;
  window.closeRequestDemoModal = closeModal;

  // 5. Attach Closing Event Listeners
  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  window.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      modal.getAttribute("aria-hidden") === "false"
    ) {
      closeModal();
    }
  });

  // 6. Automatically bind to all "Request Demo" buttons and "Request Demo" buttons
  // This looks for links to signup.html and the specific ID of your hero button
  const triggerElements = document.querySelectorAll(
    'a[href="signup.html"], #requestDemoBtn',
  );

  triggerElements.forEach((trigger) => {
    trigger.addEventListener("click", (e) => {
      e.preventDefault(); // Stops the browser from navigating to signup.html
      openModal();
    });
  });
});
