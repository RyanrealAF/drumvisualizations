class LogoOverlay {
    constructor() {
        this.container = document.getElementById('logo-container');
        this.logo = document.getElementById('logo-svg');
        this.logoPath = this.logo.querySelector('path');
        this.audio = document.getElementById('audio-track');
        
        // Initialize sub-systems
        this.particles = new ParticleSystem('particles-canvas', 800);
        
        // Data state
        this.drumData = null;
        this.cursors = { kick: 0, snare: 0, hats: 0 };
        
        // Physics state
        this.scale = 1.0;
        this.scaleVelocity = 0;
        
        this.loadDrumData();
        
        // Start animation loop
        requestAnimationFrame(() => this.animate());
    }

    async loadDrumData() {
        try {
            const response = await fetch('drum-data.json');
            this.drumData = await response.json();
            console.log("Drum data loaded successfully");
        } catch (e) {
            console.error("Failed to load drum data. Ensure analyze_drums.py has run.", e);
        }
    }

    animate() {
        // Sync triggers to audio playback
        if (this.drumData && !this.audio.paused) {
            const currentTime = this.audio.currentTime;
            this.checkTriggers(currentTime);
        }

        this.updatePhysics();
        this.particles.update();
        
        requestAnimationFrame(() => this.animate());
    }

    checkTriggers(currentTime) {
        ['kick', 'snare', 'hats'].forEach(type => {
            const hits = this.drumData[type];
            let idx = this.cursors[type];
            
            // Check for hits that occurred since the last check
            while (idx < hits.length && hits[idx][0] <= currentTime) {
                // Only trigger if the hit is very recent (within 100ms)
                // This prevents a massive explosion of visuals if the user seeks forward
                if (currentTime - hits[idx][0] < 0.1) {
                    const velocity = hits[idx][1];
                    if (type === 'kick') this.triggerKick(velocity);
                    if (type === 'snare') this.triggerSnare(velocity);
                    if (type === 'hats') this.triggerHats(velocity);
                }
                idx++;
            }
            this.cursors[type] = idx;
        });
    }

    triggerKick(velocity) {
        // Physics Impulse
        this.scaleVelocity += velocity * 0.15; 
        
        // Color Flash: Deep umber -> Rust orange
        const color = this.velocityToColor(velocity);
        this.logoPath.style.fill = color;
        
        // Radial Shockwave (Drop Shadow)
        const blur = 20 + (velocity * 60);
        const shadowColor = `rgba(220, 100, 60, ${velocity * 0.8})`;
        this.logo.style.filter = `drop-shadow(0 0 ${blur}px ${shadowColor})`;
        
        // Reset visual effects after short duration
        setTimeout(() => {
             this.logoPath.style.fill = '#3D3631'; 
             this.logo.style.filter = 'drop-shadow(0 0 0 transparent)';
        }, 100 + velocity * 200);
    }

    triggerSnare(velocity) {
        // Sharp white/cyan edge glow
        const blur = 15 + velocity * 25;
        const color = `rgba(220, 255, 255, ${velocity})`;
        this.logo.style.filter = `drop-shadow(0 0 ${blur}px ${color})`;
        
        setTimeout(() => {
            this.logo.style.filter = 'drop-shadow(0 0 0 transparent)';
        }, 150);
    }

    triggerHats(velocity) {
        this.particles.triggerHatsFlicker(velocity);
    }

    updatePhysics() {
        // Spring Physics: F = -k*x - c*v
        const k = 0.15; // Spring stiffness
        const c = 0.25; // Damping
        
        const displacement = this.scale - 1.0;
        const force = -k * displacement - c * this.scaleVelocity;
        
        this.scaleVelocity += force;
        this.scale += this.scaleVelocity;
        
        // Apply to DOM
        this.container.style.transform = `translate(-50%, -50%) scale(${this.scale})`;
    }

    velocityToColor(velocity) {
        const r = Math.floor(61 + velocity * 160);
        const g = Math.floor(54 + velocity * 46);
        const b = Math.floor(49 + velocity * 11);
        return `rgb(${r}, ${g}, ${b})`;
    }
}

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
    window.overlay = new LogoOverlay();
});