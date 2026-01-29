import React, { useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { useTexture } from '@react-three/drei';

// --- SHADERS ---

const particleVertexShader = `
  uniform float uTime;
  attribute float aAlpha;
  attribute float aFlickerPhase;
  attribute float aSize;
  varying float vAlpha;
  varying float vFlicker;

  void main() {
    vAlpha = aAlpha;
    vFlicker = 0.7 + 0.3 * sin(aFlickerPhase + uTime * 5.0);
    
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = aSize * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

const particleFragmentShader = `
  varying float vAlpha;
  varying float vFlicker;

  void main() {
    float dist = length(gl_PointCoord - 0.5);
    if (dist > 0.5) discard;
    
    float soft = smoothstep(0.5, 0.2, dist);
    gl_FragColor = vec4(0.78, 0.78, 0.86, vAlpha * vFlicker * soft);
  }
`;

const logoVertexShader = `
  varying vec2 vUv;
  uniform float uScale;
  
  void main() {
    vUv = uv;
    // Apply scale centered
    vec3 pos = position;
    pos.xy *= uScale;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`;

const logoFragmentShader = `
  varying vec2 vUv;
  uniform sampler2D uTexture;
  uniform vec3 uGlowColor;
  uniform float uGlowIntensity;

  void main() {
    vec4 texColor = texture2D(uTexture, vUv);
    if (texColor.a < 0.1) discard;
    
    // Mix base color with glow
    vec3 finalColor = texColor.rgb + uGlowColor * uGlowIntensity;
    gl_FragColor = vec4(finalColor, texColor.a);
  }
`;

// --- COMPONENTS ---

const Particles: React.FC<{ isProcessing: boolean }> = ({ isProcessing }) => {
  const count = 800;
  const meshRef = useRef<THREE.Points>(null);
  
  const [positions, alphas, phases, sizes] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const alp = new Float32Array(count);
    const pha = new Float32Array(count);
    const siz = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10; // X
      pos[i * 3 + 1] = -2.5 + (Math.random() - 0.5) * 1.5; // Y (bottom concentrated)
      pos[i * 3 + 2] = (Math.random() - 0.5) * 5; // Z
      
      alp[i] = 0.3 + Math.random() * 0.4;
      pha[i] = Math.random() * Math.PI * 2;
      siz[i] = 1.0 + Math.random() * 2.0;
    }
    return [pos, alp, pha, siz];
  }, []);

  useFrame((state) => {
    if (meshRef.current) {
      (meshRef.current.material as THREE.ShaderMaterial).uniforms.uTime.value = state.clock.elapsedTime;
      
      if (isProcessing) {
          // Subtle upward drift
          const positionsArr = meshRef.current.geometry.attributes.position.array as Float32Array;
          for(let i=0; i<count; i++) {
              positionsArr[i*3+1] += 0.005;
              if (positionsArr[i*3+1] > 2.0) positionsArr[i*3+1] = -3.0;
          }
          meshRef.current.geometry.attributes.position.needsUpdate = true;
      }
    }
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
        <bufferAttribute attach="attributes-aAlpha" count={count} array={alphas} itemSize={1} />
        <bufferAttribute attach="attributes-aFlickerPhase" count={count} array={phases} itemSize={1} />
        <bufferAttribute attach="attributes-aSize" count={count} array={sizes} itemSize={1} />
      </bufferGeometry>
      <shaderMaterial
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        vertexShader={particleVertexShader}
        fragmentShader={particleFragmentShader}
        uniforms={{ uTime: { value: 0 } }}
      />
    </points>
  );
};

const ReactiveLogo: React.FC<{ isProcessing: boolean }> = ({ isProcessing }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.ShaderMaterial>(null);
  
  // Create a canvas texture for the logo to avoid external SVG loading issues
  const logoTexture = useMemo(() => {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 512;
      const ctx = canvas.getContext('2d');
      if (ctx) {
          ctx.fillStyle = '#3D3631';
          ctx.font = 'bold 120px Inter, sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('RYAN', 256, 150);
          ctx.fillText('REAL', 256, 256);
          ctx.fillText('AF', 256, 360);
      }
      const tex = new THREE.CanvasTexture(canvas);
      return tex;
  }, []);

  const state = useRef({
      scale: 1.0,
      targetScale: 1.0,
      velocity: 0,
      glow: 0,
      targetGlow: 0
  });

  useFrame((_, delta) => {
    if (!materialRef.current) return;

    if (isProcessing) {
        // Random triggers for simulation
        if (Math.random() > 0.95) { // Kick
            state.current.targetScale = 1.2;
            state.current.velocity = 0.1;
            state.current.targetGlow = 0.8;
        }
        if (Math.random() > 0.97) { // Snare
            state.current.targetGlow = 1.0;
        }
    }

    // Spring physics
    const springStrength = 15.0;
    const damping = 0.8;
    const diff = state.current.targetScale - state.current.scale;
    state.current.velocity += diff * springStrength * delta;
    state.current.velocity *= damping;
    state.current.scale += state.current.velocity;
    
    // Decay targets
    state.current.targetScale += (1.0 - state.current.targetScale) * 0.1;
    state.current.targetGlow *= 0.9;
    state.current.glow += (state.current.targetGlow - state.current.glow) * 0.2;

    materialRef.current.uniforms.uScale.value = state.current.scale;
    materialRef.current.uniforms.uGlowIntensity.value = state.current.glow;
  });

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[4, 4]} />
      <shaderMaterial
        ref={materialRef}
        transparent
        vertexShader={logoVertexShader}
        fragmentShader={logoFragmentShader}
        uniforms={{
          uTexture: { value: logoTexture },
          uScale: { value: 1.0 },
          uGlowColor: { value: new THREE.Color(0xdc643c) },
          uGlowIntensity: { value: 0.0 }
        }}
      />
    </mesh>
  );
};

interface DrumOverlayProps {
  isProcessing: boolean;
}

const DrumOverlay: React.FC<DrumOverlayProps> = ({ isProcessing }) => {
  return (
    <div className="relative w-full aspect-video bg-[#fdfbf7] overflow-hidden rounded-2xl border-2 border-[#3D3631] shadow-[8px_8px_0px_0px_rgba(61,54,49,0.1)]">
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        <color attach="background" args={['#fdfbf7']} />
        <ambientLight intensity={1.5} />
        <Particles isProcessing={isProcessing} />
        <ReactiveLogo isProcessing={isProcessing} />
      </Canvas>
      {isProcessing && (
        <div className="absolute bottom-4 left-4 z-30 bg-[#3D3631] text-white px-3 py-1 rounded-none font-black text-[10px] tracking-widest border-l-4 border-[#D2643C]">
          ⚡ GPU PROCESSING ACTIVE
        </div>
      )}
    </div>
  );
};

export default DrumOverlay;
