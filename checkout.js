/**
 * Checkout & Consultation Flow Script
 * WorkMerate Payment Flow
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global State for checkout flow data
  const checkoutData = {
    plan: 'Starter',
    company_name: 'Acme Corporation',
    industry: 'Manufacturing',
    business_type: 'Corporation',
    employees: '11 - 50',
    country: 'Nigeria',
    state_city: 'Lagos',
    website: 'https://www.acme.com',
    full_name: 'John Doe',
    job_title: 'Manager',
    work_email: 'john@acme.com',
    department: 'IT',
    phone_number: '0800000012',
    contact_method: 'Whatsapp',
    is_decision_maker: true,
    is_evaluating: false,
    business_situation: 'Spreadsheet',
    modules: ['Finance', 'Sales', 'CRM'],
    challenges: ['Manual Processes', 'Data fragmentation'],
    timeline: '4 weeks',
    budget: '500k',
    date: 'Thursday, Oct 24, 2026',
    time_slot: '11:30 AM',
    platform: 'Google Meet'
  };

  // Parse URL Parameters
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('plan')) {
    checkoutData.plan = urlParams.get('plan');
  }

  // DOM Elements
  const stepPanes = document.querySelectorAll('.step-pane');
  const stepperItems = document.querySelectorAll('.stepper-item');

  // ==================== STEPPER NAVIGATION ====================
  function goToStep(stepNumber) {
    const target = parseInt(stepNumber, 10);
    if (isNaN(target) || target < 1 || target > 6) return;

    // Update Panes
    stepPanes.forEach(pane => {
      const paneStep = parseInt(pane.getAttribute('data-step'), 10);
      if (paneStep === target) {
        pane.classList.add('active');
      } else {
        pane.classList.remove('active');
      }
    });

    // Update Stepper Nav Items
    stepperItems.forEach(item => {
      const itemStep = parseInt(item.getAttribute('data-step-target'), 10);
      item.classList.remove('active', 'completed');
      if (itemStep === target) {
        item.classList.add('active');
      } else if (itemStep < target) {
        item.classList.add('completed');
      }
    });

    // Update Review Summary if entering Step 5
    if (target === 5) {
      updateReviewSummary();
    }

    // Update Done Screen if entering Step 6
    if (target === 6) {
      updateDoneScreen();
    }

    // Scroll to top of main box
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Next Buttons
  document.querySelectorAll('[data-next-step]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const nextStep = e.currentTarget.getAttribute('data-next-step');
      collectCurrentStepData();
      goToStep(nextStep);
    });
  });

  // Prev Buttons
  document.querySelectorAll('[data-prev-step]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const prevStep = e.currentTarget.getAttribute('data-prev-step');
      goToStep(prevStep);
    });
  });

  // Sidebar Direct Click
  stepperItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetStep = item.getAttribute('data-step-target');
      collectCurrentStepData();
      goToStep(targetStep);
    });
  });

  // ==================== CUSTOM DROPDOWN SYSTEM ====================
  const customDropdowns = document.querySelectorAll('.custom-dropdown');

  customDropdowns.forEach(dropdown => {
    const trigger = dropdown.querySelector('.dropdown-trigger');
    const selectedText = dropdown.querySelector('.selected-text');
    const items = dropdown.querySelectorAll('.dropdown-item');
    const key = dropdown.getAttribute('data-dropdown');

    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      customDropdowns.forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
      });
      dropdown.classList.toggle('open');
    });

    items.forEach(item => {
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        const value = item.getAttribute('data-value');
        selectedText.textContent = value;
        selectedText.classList.remove('placeholder');
        dropdown.classList.remove('open');

        if (key && checkoutData.hasOwnProperty(key)) {
          checkoutData[key] = value;
        }
      });
    });
  });

  document.addEventListener('click', () => {
    customDropdowns.forEach(d => d.classList.remove('open'));
  });

  // ==================== STEP 3: RADIO CARDS ====================
  const radioCards = document.querySelectorAll('.selection-card');
  radioCards.forEach(card => {
    card.addEventListener('click', () => {
      radioCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      const radio = card.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
        checkoutData.business_situation = radio.value;
      }
    });
  });

  // Module Pills Multi-select
  const modulePills = document.querySelectorAll('.module-pill');
  modulePills.forEach(pill => {
    pill.addEventListener('click', () => {
      pill.classList.toggle('selected');
      const modName = pill.getAttribute('data-module');
      if (pill.classList.contains('selected')) {
        if (!checkoutData.modules.includes(modName)) {
          checkoutData.modules.push(modName);
        }
      } else {
        checkoutData.modules = checkoutData.modules.filter(m => m !== modName);
      }
    });
  });

  // Challenge Chips Multi-select
  const challengeChips = document.querySelectorAll('.challenge-chip');
  challengeChips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('selected');
      const name = chip.getAttribute('data-challenge');
      if (chip.classList.contains('selected')) {
        if (!checkoutData.challenges.includes(name)) {
          checkoutData.challenges.push(name);
        }
      } else {
        checkoutData.challenges = checkoutData.challenges.filter(c => c !== name);
      }
    });
  });

  // ==================== STEP 4: CALENDAR & TIME SLOTS ====================
  let currentDate = new Date(2026, 9, 24); // October 24, 2026
  let selectedDay = 24;

  const calMonthTitle = document.getElementById('cal-month-title');
  const calDaysGrid = document.getElementById('cal-days-grid');
  const prevMonthBtn = document.getElementById('cal-prev');
  const nextMonthBtn = document.getElementById('cal-next');

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    if (calMonthTitle) {
      calMonthTitle.textContent = `${monthNames[month]} ${year}`;
    }

    if (!calDaysGrid) return;
    calDaysGrid.innerHTML = '';

    const firstDayIndex = new Date(year, month, 1).getDay();
    const totalDays = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDayIndex; i++) {
      const emptySpan = document.createElement('div');
      emptySpan.className = 'cal-day empty';
      calDaysGrid.appendChild(emptySpan);
    }

    for (let day = 1; day <= totalDays; day++) {
      const dayBtn = document.createElement('div');
      dayBtn.className = 'cal-day';
      dayBtn.textContent = day;

      if (day === selectedDay) {
        dayBtn.classList.add('active');
      }

      dayBtn.addEventListener('click', () => {
        document.querySelectorAll('.cal-day').forEach(d => d.classList.remove('active'));
        dayBtn.classList.add('active');
        selectedDay = day;
        checkoutData.date = `Thursday, ${monthNames[month].slice(0,3)} ${day}, ${year}`;
      });

      calDaysGrid.appendChild(dayBtn);
    }
  }

  if (prevMonthBtn && nextMonthBtn) {
    prevMonthBtn.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      renderCalendar();
    });

    nextMonthBtn.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      renderCalendar();
    });
  }

  renderCalendar();

  // Time Slot buttons
  const timeSlotBtns = document.querySelectorAll('.time-slot-btn');
  timeSlotBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      timeSlotBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      checkoutData.time_slot = btn.getAttribute('data-time');
    });
  });

  // Platform buttons
  const platformBtns = document.querySelectorAll('.platform-btn');
  platformBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      platformBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      checkoutData.platform = btn.getAttribute('data-platform');
    });
  });

  // ==================== COLLECT & SYNC DATA ====================
  function collectCurrentStepData() {
    // Step 1
    const compNameInput = document.getElementById('company_name');
    if (compNameInput && compNameInput.value) checkoutData.company_name = compNameInput.value;

    const stateCityInput = document.getElementById('state_city');
    if (stateCityInput && stateCityInput.value) checkoutData.state_city = stateCityInput.value;

    const websiteInput = document.getElementById('website');
    if (websiteInput && websiteInput.value) checkoutData.website = websiteInput.value;

    // Step 2
    const fullNameInput = document.getElementById('full_name');
    if (fullNameInput && fullNameInput.value) checkoutData.full_name = fullNameInput.value;

    const jobTitleInput = document.getElementById('job_title');
    if (jobTitleInput && jobTitleInput.value) checkoutData.job_title = jobTitleInput.value;

    const emailInput = document.getElementById('work_email');
    if (emailInput && emailInput.value) checkoutData.work_email = emailInput.value;

    const deptInput = document.getElementById('department');
    if (deptInput && deptInput.value) checkoutData.department = deptInput.value;

    const phoneInput = document.getElementById('phone_number');
    if (phoneInput && phoneInput.value) checkoutData.phone_number = phoneInput.value;
  }

  function updateReviewSummary() {
    collectCurrentStepData();

    // Company Info Card
    const revCompName = document.getElementById('rev-company-name');
    if (revCompName) revCompName.textContent = checkoutData.company_name || 'Acme Corporation';

    const revIndustry = document.getElementById('rev-industry');
    if (revIndustry) revIndustry.textContent = checkoutData.industry || 'Manufacturing';

    // Primary Contact Card
    const revContactName = document.getElementById('rev-contact-name');
    if (revContactName) revContactName.textContent = checkoutData.full_name || 'John Doe';

    const revContactEmail = document.getElementById('rev-contact-email');
    if (revContactEmail) revContactEmail.textContent = checkoutData.work_email || 'john@acme.com';

    // ERP Requirements Modules Tags
    const revModulesList = document.getElementById('rev-modules-list');
    if (revModulesList) {
      revModulesList.innerHTML = '';
      const displayMods = checkoutData.modules.length > 0 ? checkoutData.modules : ['Finance', 'Sales', 'CRM'];
      displayMods.forEach(mod => {
        const tag = document.createElement('span');
        tag.className = 'mod-tag';
        tag.textContent = mod;
        revModulesList.appendChild(tag);
      });
    }

    // Meeting Details
    const revMeetingStr = document.getElementById('rev-meeting-str');
    if (revMeetingStr) {
      revMeetingStr.textContent = `${checkoutData.date.replace(/, \d{4}/, '')} • ${checkoutData.time_slot} (${checkoutData.platform})`;
    }
  }

  function updateDoneScreen() {
    const doneUserEmail = document.getElementById('done-user-email');
    if (doneUserEmail) doneUserEmail.textContent = checkoutData.work_email || 'john@acme.com';

    const doneDateStr = document.getElementById('done-date-str');
    if (doneDateStr) doneDateStr.textContent = checkoutData.date || 'Thursday, October 24, 2026';

    const doneTimeStr = document.getElementById('done-time-str');
    if (doneTimeStr) doneTimeStr.textContent = `${checkoutData.time_slot} - 12:30 PM`;

    const donePlatformStr = document.getElementById('done-platform-str');
    if (donePlatformStr) donePlatformStr.textContent = checkoutData.platform || 'Google Meet';
  }

  // ==================== EDIT MODALS SYSTEM ====================
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('open');
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('open');
  }

  // Modal Close buttons
  document.querySelectorAll('[data-modal-close]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const backdrop = e.target.closest('.modal-backdrop');
      if (backdrop) backdrop.classList.remove('open');
    });
  });

  // Modal Backdrop Click
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) backdrop.classList.remove('open');
    });
  });

  // Edit Company Button
  const editCompanyBtn = document.getElementById('edit-company-btn');
  if (editCompanyBtn) {
    editCompanyBtn.addEventListener('click', () => {
      document.getElementById('modal_company_name').value = checkoutData.company_name;
      document.getElementById('modal_industry_val').textContent = checkoutData.industry || 'Manufacturing';
      openModal('modal-company');
    });
  }

  const saveCompanyBtn = document.getElementById('save-company-btn');
  if (saveCompanyBtn) {
    saveCompanyBtn.addEventListener('click', () => {
      checkoutData.company_name = document.getElementById('modal_company_name').value;
      checkoutData.industry = document.getElementById('modal_industry_val').textContent;
      updateReviewSummary();
      closeModal('modal-company');
    });
  }

  // Edit Contact Button
  const editContactBtn = document.getElementById('edit-contact-btn');
  if (editContactBtn) {
    editContactBtn.addEventListener('click', () => {
      document.getElementById('modal_contact_name').value = checkoutData.full_name;
      document.getElementById('modal_contact_email').value = checkoutData.work_email;
      openModal('modal-contact');
    });
  }

  const saveContactBtn = document.getElementById('save-contact-btn');
  if (saveContactBtn) {
    saveContactBtn.addEventListener('click', () => {
      checkoutData.full_name = document.getElementById('modal_contact_name').value;
      checkoutData.work_email = document.getElementById('modal_contact_email').value;
      updateReviewSummary();
      closeModal('modal-contact');
    });
  }

  // Edit ERP Requirements Button
  const editErpBtn = document.getElementById('edit-erp-btn');
  if (editErpBtn) {
    editErpBtn.addEventListener('click', () => {
      openModal('modal-erp');
    });
  }

  const saveErpBtn = document.getElementById('save-erp-btn');
  if (saveErpBtn) {
    saveErpBtn.addEventListener('click', () => {
      const selectedPills = document.querySelectorAll('#modal-modules-wrap .module-pill.selected');
      checkoutData.modules = Array.from(selectedPills).map(p => p.getAttribute('data-module'));
      updateReviewSummary();
      closeModal('modal-erp');
    });
  }

  // Edit Meeting Button
  const editMeetingBtn = document.getElementById('edit-meeting-btn');
  if (editMeetingBtn) {
    editMeetingBtn.addEventListener('click', () => {
      document.getElementById('modal_date_val').value = checkoutData.date;
      document.getElementById('modal_time_val').value = checkoutData.time_slot;
      document.getElementById('modal_platform_val').textContent = checkoutData.platform;
      openModal('modal-meeting');
    });
  }

  const saveMeetingBtn = document.getElementById('save-meeting-btn');
  if (saveMeetingBtn) {
    saveMeetingBtn.addEventListener('click', () => {
      checkoutData.date = document.getElementById('modal_date_val').value;
      checkoutData.time_slot = document.getElementById('modal_time_val').value;
      checkoutData.platform = document.getElementById('modal_platform_val').textContent;
      updateReviewSummary();
      closeModal('modal-meeting');
    });
  }
});
