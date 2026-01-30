class Particle {
    constructor(canvasWidth, canvasHeight) {
        this.w = canvasWidth;
        this.h = canvasHeight;
        this.reset();
    }
    
    reset() {
        this.x = Math.random() * this.w;
        // Concentrated in bottom 30%
        this.y = this.h * (0.7 + Math.random() * 0.3); 
        
        // Physics: Upward drift with slight horizontal jitter
        this.vx = (Math.random() - 0.5) * 0.6; 
        this.vy = -0.2 - (Math.random() * 0.3); 
        
        this.size = 1 + Math.random() * 2; 
        this.baseAlpha = 0.3 + Math.random() * 0.4; 
        this.phase = Math.random() * Math.PI * 2;
        this.flickerIntensity = 0;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.phase += 0.05;

        // Wrap around boundaries
        if (this.y < 0) this.y = this.h;
        if (this.x > this.w) this.x = 0;
        if (this.x < 0) this.x = this.w;
        
        // Decay flicker effect from hats
        this.flickerIntensity *= 0.9;
    }

    draw(ctx) {
        const flicker = Math.sin(this.phase) * 0.2 * this.flickerIntensity;
        const alpha = Math.max(0, Math.min(1, this.baseAlpha + flicker));
        
        ctx.fillStyle = `rgba(200, 200, 220, ${alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

class ParticleSystem {
    constructor(canvasId, count) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.count = count;
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        this.initParticles();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    initParticles() {
        for (let i = 0; i < this.count; i++) {
            this.particles.push(new Particle(this.canvas.width, this.canvas.height));
        }
    }

    triggerHatsFlicker(velocity) {
        this.particles.forEach(p => {
            // Add intensity based on velocity
            p.flickerIntensity = Math.max(p.flickerIntensity, velocity * 2.0);
        });
    }

    update() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.particles.forEach(p => {
            p.update();
            p.draw(this.ctx);
        });
    }
}