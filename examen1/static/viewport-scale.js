(() => {
    const BASE_WIDTH = 2560;
    const BASE_HEIGHT = 1440;
    const SCALE_MODE = 'cover';

    function applyScale() {
        const body = document.body;
        if (!body) return;

        const scaleFn = SCALE_MODE === 'cover' ? Math.max : Math.min;
        const scale = scaleFn(window.innerWidth / BASE_WIDTH, window.innerHeight / BASE_HEIGHT);
        const offsetX = (window.innerWidth - BASE_WIDTH * scale) / 2;
        const offsetY = (window.innerHeight - BASE_HEIGHT * scale) / 2;

        document.documentElement.style.overflow = 'hidden';
        body.style.overflow = 'hidden';
        body.style.width = `${BASE_WIDTH}px`;
        body.style.height = `${BASE_HEIGHT}px`;
        body.style.transformOrigin = 'top left';
        body.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
    }

    window.addEventListener('resize', applyScale);
    window.addEventListener('orientationchange', applyScale);
    window.addEventListener('load', applyScale);
    applyScale();
})();
