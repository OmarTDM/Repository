(() => {
    const ingredientButtons = document.querySelectorAll('.ingredient-btn');
    const overlay = document.getElementById('cinematic-overlay');

    if (!ingredientButtons.length || !overlay) {
        return;
    }

    const panels = [
        overlay.querySelector('.cinematic-panel-left'),
        overlay.querySelector('.cinematic-panel-middle'),
        overlay.querySelector('.cinematic-panel-right'),
    ];

    const dingBack = document.getElementById('cinematic-ding-back');
    const dingScreen = document.getElementById('cinematic-ding');
    let running = false;

    const closeCinematic = () => {
        dingBack.classList.remove('ding-back-visible');
        dingScreen.classList.remove('ding-visible');
        setTimeout(() => {
            overlay.classList.remove('cinematic-slidedown');
            panels.forEach((p) => p.classList.remove('panel-visible'));
            running = false;
        }, 600);
    };

    if (dingBack) {
        dingBack.addEventListener('click', closeCinematic);
    }

    const runCinematic = () => {
        if (running) {
            return;
        }
        running = true;

        // Reset state
        overlay.classList.remove('cinematic-slidedown');
        panels.forEach((p) => p.classList.remove('panel-visible'));

        // Fade in black overlay
        overlay.classList.add('cinematic-visible');

        // Left panel slides in
        setTimeout(() => panels[0] && panels[0].classList.add('panel-visible'), 550);

        // Middle panel fades in
        setTimeout(() => panels[1] && panels[1].classList.add('panel-visible'), 1200);

        // Right panel fades in
        setTimeout(() => panels[2] && panels[2].classList.add('panel-visible'), 1850);

        // Slide all panels down → reveal ding screen
        setTimeout(() => {
            overlay.classList.add('cinematic-slidedown');

            // Once panels are off-screen, fade overlay out and show ding on top
            setTimeout(() => {
                overlay.classList.remove('cinematic-visible');
                dingScreen.classList.add('ding-visible');
            }, 500);

            // Show back button once ding screen is fully visible
            setTimeout(() => {
                dingBack.classList.add('ding-back-visible');
            }, 1100);
        }, 3400);
    };

    ingredientButtons.forEach((btn) => {
        btn.addEventListener('click', runCinematic);
    });
})();
